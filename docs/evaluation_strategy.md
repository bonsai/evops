# evops 評価戦略 — ローカル / Kaggle / JEV

## 方針

| タスク | 環境 | 理由 |
|--------|------|------|
| 基本評価（サイズ・色・CLIP） | **ローカル CPU** | 軽量・リアルタイム |
| 動画メトリクス（FFprobe） | **ローカル CPU** | フレーム解析不要 |
| ML 評価（大規模モデル） | **Kaggle GPU** | VRAM 節約・バッチ処理 |
| エフェクト品質（主観的） | **JEV** | Jupyter 可視化・人間フィードバック |
| 生成（bpy / 動画レンダリング） | **ローカル GPU or Kaggle** | Blender / ffmpeg CUDA |

## ローカル評価（evops デフォルト）

```bash
# MCP evaluator（port 8002）をローカル起動
python mcp/evaluator/server.py --http --port 8002

# 評価対象
- clip_text_similarity
- clip_image_similarity
- basic_image_metrics
- color_statistics
- video_metrics
- ascii_art_metrics
- effect_metrics
```

## Kaggle GPU 連携

```yaml
# workflow.yaml 内の Kaggle ステップ例
- id: kaggle_eval
  name: Kaggle GPU Evaluation
  type: kaggle_notebook
  notebook: evops/kaggle/eval_clip_gpu.ipynb
  inputs:
    - image_dir: $WORKSPACE/svg/
  outputs:
    - eval_result.json
```

### Kaggle Notebook テンプレート

```python
# kaggle/eval_clip_gpu.ipynb（簡易版）
import torch, clip, json, glob
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

results = {}
for path in glob.glob("/kaggle/input/evops-images/*.png"):
    image = preprocess(Image.open(path)).unsqueeze(0).to(device)
    text = clip.tokenize(["a 4-panel manga illustration"]).to(device)
    with torch.no_grad():
        logits = model(image, text)
        results[path] = {"clip_score": float(logits[0][0])}

with open("/kaggle/working/eval_result.json", "w") as f:
    json.dump(results, f)
```

## JEV（Jupyter Evaluation Visualizer）連携

```bash
# JEV は Jupyter Notebook ベースの主観的評価ツール
# 人間が画像/動画を見てスコアを入力し、結果を JSON で出力
pip install jev  # 仮想パッケージ名
jev launch $WORKSPACE/artifacts/ --out eval_human.json
```

## ワークフロー統合

```yaml
# workflow.yaml における評価ステップ
steps:
  - id: eval_local
    name: Local Evaluation
    cmd: python mcp/evaluator/scripts/batch_eval.py --images svg/
  - id: eval_kaggle
    name: Kaggle GPU Evaluation
    cmd: kaggle kernels push evops/eval-gpu --wait
  - id: eval_jev
    name: Human Evaluation (JEV)
    cmd: jev launch $WORKSPACE/artifacts --out eval_human.json
```

## GPU 活用ルール

- **生成時**: `bpy-gen`（Blender）のサンプリング数を上げても Kaggle の P100/T4 で OK
- **評価時**: CLIP 大規模モデルのバッチ推論のみ GPU を使用
- **ローカル 16GB CPU 環境**では、生成は低解像度・低サンプルで実施
