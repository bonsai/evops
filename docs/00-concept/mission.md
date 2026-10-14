# Mission — Evaluate Operations

## 本質問

生成AIの出力品質を、**生成後に評価し、評価結果をフィードバックして次の生成を進化させる**、この閉ループを自動化せよ。

## 三原則

1. **Generation is cheap. Evaluation is the bottleneck.**
   - 生成コストは下がり続けるが、品質評価は人間に依存しがち
   -  Evaluator を自動化し、スケールさせる

2. **Intent → Metric → Action**
   - ユーザーの意図（Intent）を構造化し、それを測定可能な指標（Metric）に変換
   - 指標に基づいて次のアクションを自動決定

3. **Wide Gate → Narrow Gate**
   - 開発中は**Wide Gate**（閾値低め、完了を優先）
   - 品質フィルタ時は**Narrow Gate**（閾値高め、厳選を優先）

## 7つのユーザ意図（Extracted）

1. 論文調査 → 4コマSF落語 → 映像生成
2. 独創性評価＋動画スコアリング
3. ブラックボックス回避＋DSL可視化
4. Chaperoneによる完全自動化
5. 多言語・ディープな字幕スタイル
6. 3Dモデルを2Dアニメカットに変換
7. 映像生成の自動評価ループ
