# MVP — Doraemon Evolution Loop

## Goal
2D POCで確認した評価ループを、Blender/bpyを中心とした3D生成・進化ループへ拡張する。

## Flow
Intent + Reference → Method / Genome → Generate → Render → VLM + Numeric Evaluation → Fitness → DB → Selection → Mutation / Crossover / Repair / Kill → Next Generation → Growth Animation

## Genome
- head/body proportions
- eye size / position
- face geometry
- material / color
- camera
- lighting
- primitive strategy
- generation code

## Fitness
fitness = similarity + intent_alignment - λ complexity - μ runtime - ν code_size

初期値は仮説として設定し、実験データから調整する。

## MVP Success Criteria
- 複数Generationを自動生成できる
- Candidate / Evaluation / FitnessをDBへ保存できる
- Selectionが次世代へ反映される
- Fitness推移を記録できる
- 低Fitness候補をRepairまたはKillできる
- 最終的にMP4の成長アニメーションを生成できる
- 同じデータから実験を再現できる