// cmd/bqmlite: CLI entry point (BQML-style, deterministic, no deps).
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"github.com/bonsai/bqmlite-go/bqmlite"
)

func main() {
	in := flag.String("input", "", "dataset.json or plan.json path")
	out := flag.String("output", "", "output path")
	engine := flag.String("engine", "", "engine: mean|linear_regression|logistic_regression")
	flag.Parse()

	data, err := os.ReadFile(*in)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	p := bqmlite.Plan{Engine: *engine}
	var raw map[string]json.RawMessage
	if err := json.Unmarshal(data, &raw); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if _, hasPlan := raw["plan"]; hasPlan {
		if err := json.Unmarshal(data, &p); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
	} else {
		// raw Dataset shape: {name, target, rows}
		if err := json.Unmarshal(data, &p.Dataset); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
	}
	res, err := bqmlite.ExecuteJSON(&p)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	outMap := map[string]any{
		"result":      res,
		"fingerprint": res.Fingerprint(),
	}
	if p.Rows != nil {
		outMap["mode"] = "predict"
	} else {
		outMap["mode"] = "train+predict"
	}
	b, _ := json.MarshalIndent(outMap, "", "  ")
	b = append(b, '\n')
	if *out != "" {
		if err := os.WriteFile(*out, b, 0o644); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
	} else {
		os.Stdout.Write(b)
	}
	fmt.Printf("fingerprint: %s\n", res.Fingerprint())
}
