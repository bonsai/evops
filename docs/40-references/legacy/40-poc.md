# POC — 2D Evaluation Loop

## Purpose
本丸の3D進化ループへ進む前に、最小構成で「生成 → 評価 → 修正 → 再生成」が成立することを確認する。

## Scope
対象はSVG/CSSまたはPygameによる2Dアニメーション。

## Flow
Reference → Candidate SVG → Render PNG/MP4 → VLM/LMS Evaluation → Good / Bad / Score → Repair → Re-render → Compare

## POC Data

    candidate_id: poc-001
    generation: 0
    renderer: svg
    reference: reference.png
    artifact: candidate.mp4
    evaluation: similarity / intent_alignment / readability
    fitness: 0.0

## POC Success Criteria
- 1つのReferenceから複数Candidateを生成できる
- VLM/LMSで比較評価できる
- 評価をJSONLへ保存できる
- 評価結果から1項目以上を修正できる
- 修正前後を比較できる
- MP4をArtifactとして回収できる

## Out of Scope
Blenderによる本格3D、GA全機能、長時間学習はMVPへ回す。