// Package bqmlite implements a deterministic, dependency-free BigQuery-ML-like
// engine: mean / linear_regression (normal equations) / logistic_regression
// (batch GD). Input/output follow the Dataset / Plan / PredictionResult shapes.
package bqmlite

import (
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"math"
	"sort"
)

// Dataset is the training/input data shape (JSON or Plan).
type Dataset struct {
	Name   string            `json:"name"`
	Target string            `json:"target"`
	Rows   []map[string]any  `json:"rows"`
}

// Plan is the agent boundary payload for ExecuteJSON.
type Plan struct {
	Dataset *Dataset     `json:"dataset"`
	Engine  string       `json:"engine"`
	Rows    []map[string]any `json:"rows"` // nil -> train+predict on dataset rows
}

// PredictionResult is the engine output shape.
type PredictionResult struct {
	Engine     string              `json:"model_name"`
	Parameters map[string]any      `json:"parameters,omitempty"`
	Results    []Prediction        `json:"results"`
}

// Prediction holds a single prediction value (and optionally probability).
type Prediction struct {
	Value       float64  `json:"value"`
	Probability *float64 `json:"probability,omitempty"`
}

// PlanFingerprint returns a stable SHA-256 over the plan JSON (determinism key).
func PlanFingerprint(p *Plan) string {
	b, _ := json.Marshal(p)
	return "sha256:" + fmt.Sprintf("%x", sha256.Sum256(b))
}

// ResultFingerprint returns a stable SHA-256 over the result JSON.
func ResultFingerprint(engine string, params map[string]any, res []Prediction) string {
	b, _ := json.Marshal(struct {
		Engine  string         `json:"engine"`
		Params  map[string]any `json:"params"`
		Results []Prediction   `json:"results"`
	}{Engine: engine, Params: params, Results: res})
	return "sha256:" + fmt.Sprintf("%x", sha256.Sum256(b))
}

// numberVal converts a JSON value to float64.
func numberVal(v any) (float64, bool) {
	switch x := v.(type) {
	case float64:
		return x, true
	case int:
		return float64(x), true
	case int64:
		return float64(x), true
	case json.Number:
		n, _ := x.Float64()
		return n, true
	}
	return 0, false
}

// numericCols returns numeric columns other than target, in name order (deterministic).
func (ds *Dataset) numericCols() ([]string, error) {
	if len(ds.Rows) == 0 {
		return nil, fmt.Errorf("dataset has no rows")
	}
	cols := make([]string, 0, len(ds.Rows[0]))
	for k := range ds.Rows[0] {
		if k != ds.Target {
			cols = append(cols, k)
		}
	}
	sort.Strings(cols)
	for _, c := range cols {
		for _, r := range ds.Rows {
			if _, ok := numberVal(r[c]); !ok {
				return nil, fmt.Errorf("feature %q is not numeric", c)
			}
		}
	}
	for _, r := range ds.Rows {
		if _, ok := numberVal(r[ds.Target]); !ok {
			return nil, fmt.Errorf("target %q is not numeric", ds.Target)
		}
	}
	return cols, nil
}

func meanEngine(ds *Dataset) (*PredictionResult, error) {
	if _, err := ds.numericCols(); err != nil {
		return nil, err
	}
	var sum float64
	for _, r := range ds.Rows {
		v, _ := numberVal(r[ds.Target])
		sum += v
	}
	mean := sum / float64(len(ds.Rows))
	res := make([]Prediction, len(ds.Rows))
	for i := range res {
		res[i].Value = mean
	}
	return &PredictionResult{Engine: "mean", Results: res}, nil
}

// linearRegressionEngine: OLS via normal equations, w = (X'X)^-1 X'y.
func linearRegressionEngine(ds *Dataset) (*PredictionResult, error) {
	features, err := ds.numericCols()
	if err != nil {
		return nil, err
	}
	n := len(ds.Rows)
	m := len(features)

	X := make([][]float64, n)
	y := make([]float64, n)
	for i, r := range ds.Rows {
		row := make([]float64, m+1)
		row[0] = 1.0
		for j, f := range features {
			v, _ := numberVal(r[f])
			row[j+1] = v
		}
		X[i] = row
		v, _ := numberVal(r[ds.Target])
		y[i] = v
	}

	p := m + 1
	XtX := make([][]float64, p)
	for i := range XtX {
		XtX[i] = make([]float64, p)
	}
	Xty := make([]float64, p)
	for i := 0; i < n; i++ {
		for a := 0; a < p; a++ {
			for b := 0; b < p; b++ {
				XtX[a][b] += X[i][a] * X[i][b]
			}
			Xty[a] += X[i][a] * y[i]
		}
	}

	A := clone2D(XtX)
	I := make([][]float64, p)
	for i := range I {
		I[i] = make([]float64, p)
		I[i][i] = 1.0
	}
	w := gaussJordan(A, I)[0]

	weights := make(map[string]float64)
	weights["intercept"] = w[0]
	for j, f := range features {
		weights[f] = w[j+1]
	}

	res := make([]Prediction, n)
	for i, row := range X {
		var pred float64
		for j := 0; j < p; j++ {
			pred += row[j] * w[j]
		}
		res[i].Value = pred
	}
	return &PredictionResult{
		Engine: "linear_regression",
		Parameters: map[string]any{
			"intercept": w[0],
			"weights":   weights,
			"features":  features,
		},
		Results: res,
	}, nil
}

func clone2D(a [][]float64) [][]float64 {
	out := make([][]float64, len(a))
	for i := range a {
		out[i] = make([]float64, len(a[i]))
		copy(out[i], a[i])
	}
	return out
}

// gaussJordan solves AX = B by Gauss-Jordan in-place on a copy; returns B solution.
func gaussJordan(A, B [][]float64) [][]float64 {
	n := len(A)
	m := len(B[0])
	M := make([][]float64, n)
	for i := 0; i < n; i++ {
		M[i] = make([]float64, n+m)
		for j := 0; j < n; j++ {
			M[i][j] = A[i][j]
		}
		for j := 0; j < m; j++ {
			M[i][n+j] = B[i][j]
		}
	}

	for col := 0; col < n; col++ {
		piv := col
		for r := col + 1; r < n; r++ {
			if math.Abs(M[r][col]) > math.Abs(M[piv][col]) {
				piv = r
			}
		}
		M[col], M[piv] = M[piv], M[col]
		if math.Abs(M[col][col]) < 1e-12 {
			continue
		}
		for r := 0; r < n; r++ {
			if r != col && math.Abs(M[r][col]) > 1e-12 {
				f := M[r][col] / M[col][col]
				for c := col; c < n+m; c++ {
					M[r][c] -= f * M[col][c]
				}
			}
		}
	}

	out := make([][]float64, n)
	for i := 0; i < n; i++ {
		out[i] = make([]float64, m)
		for j := 0; j < m; j++ {
			out[i][j] = M[i][n+j]
		}
	}
	return out
}

// logisticRegressionEngine: batch gradient descent (1000 epochs, lr=0.1), target 0/1 only.
func logisticRegressionEngine(ds *Dataset) (*PredictionResult, error) {
	features, err := ds.numericCols()
	if err != nil {
		return nil, err
	}
	n := len(ds.Rows)
	m := len(features)
	if n == 0 {
		return nil, fmt.Errorf("dataset has no rows")
	}
	for _, r := range ds.Rows {
		v, ok := numberVal(r[ds.Target])
		if !ok || (v != 0 && v != 1) {
			return nil, fmt.Errorf("logistic target must be 0/1, got %v", v)
		}
	}
	sigmoid := func(z float64) float64 {
		if z < -500 {
			return 0.0
		}
		if z > 500 {
			return 1.0
		}
		return 1.0 / (1.0 + math.Exp(-z))
	}

	X := make([][]float64, n)
	y := make([]float64, n)
	for i, r := range ds.Rows {
		row := make([]float64, m+1)
		row[0] = 1.0
		for j, f := range features {
			v, _ := numberVal(r[f])
			row[j+1] = v
		}
		X[i] = row
		v, _ := numberVal(r[ds.Target])
		y[i] = v
	}

	w := make([]float64, m+1)
	lr, epochs := 0.1, 1000
	for epoch := 0; epoch < epochs; epoch++ {
		grad := make([]float64, m+1)
		for i := 0; i < n; i++ {
			var z float64
			for j := 0; j < m+1; j++ {
				z += X[i][j] * w[j]
			}
			p := sigmoid(z)
			e := p - y[i]
			for j := 0; j < m+1; j++ {
				grad[j] += e * X[i][j]
			}
		}
		for j := 0; j < m+1; j++ {
			w[j] -= lr * grad[j] / float64(n)
		}
	}

	res := make([]Prediction, n)
	for i, row := range X {
		var z float64
		for j := 0; j < m+1; j++ {
			z += row[j] * w[j]
		}
		p := sigmoid(z)
		res[i].Value = 0.0
		if p >= 0.5 {
			res[i].Value = 1.0
		}
		pp := p
		res[i].Probability = &pp
	}
	weights := make(map[string]float64)
	weights["intercept"] = w[0]
	for j, f := range features {
		weights[f] = w[j+1]
	}
	return &PredictionResult{
		Engine: "logistic_regression",
		Parameters: map[string]any{
			"weights":        weights,
			"features":       features,
			"epochs":         epochs,
			"learning_rate":  lr,
		},
		Results: res,
	}, nil
}

// Run executes a plan.
func Run(p *Plan) (*PredictionResult, error) {
	ds := p.Dataset
	if ds == nil || ds.Target == "" || len(ds.Rows) == 0 {
		return nil, fmt.Errorf("invalid plan: need dataset with target and rows")
	}
	var res *PredictionResult
	var err error
	switch p.Engine {
	case "mean":
		res, err = meanEngine(ds)
	case "linear_regression":
		res, err = linearRegressionEngine(ds)
	case "logistic_regression":
		res, err = logisticRegressionEngine(ds)
	default:
		return nil, fmt.Errorf("unknown engine: %s", p.Engine)
	}
	if err != nil {
		return nil, err
	}
	return res, nil
}

// ExecuteJSON is the public agent boundary: plan -> PredictionResult.
func ExecuteJSON(p *Plan) (*PredictionResult, error) {
	return Run(p)
}

// Fingerprint returns sha256:.. of the result JSON.
func (res *PredictionResult) Fingerprint() string {
	return ResultFingerprint(res.Engine, res.Parameters, res.Results)
}
