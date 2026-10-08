---
description: "SF論文アニメをAWで設計し、決定的なRender WFへ渡す"
intent: "論文の研究知識をSF四コマSVGから再利用可能なMP4エピソードへ変換し、成果物をArtifactとして回収できる状態にする"
on:
  workflow_dispatch:
permissions:
  contents: read
safe-outputs:
  dispatch-workflow:
    workflows: [sf-paper-animation-render]
    max: 1
---

# SF Paper Animation Orchestrator

## Task

papers/youtube/comics/P01.svg〜P25.svg を研究アニメーションの一次素材として扱う。

1. skills/sf-paper-comic/skill.md の「問題→異変→発明→研究接続」ルールを確認する。
2. 各SVGについて、論文の事実とSF演出が混ざっていないか確認する。
3. 研究上の核心が4コマだけで伝わるかを確認する。
4. 問題がなければ sf-paper-animation-render を dispatch して、決定的なSVG→MP4変換を実行する。
5. 実験結果を創作してはいけない。必要なら noop で理由を報告する。

## Output

- P01〜P25 のMP4
- GitHub Actions Artifact: sf-paper-animation-mp4
- 生成物のmanifest

## Design

AW = 判断・オーケストレーション。
Render WF = 決定的な変換・Artifact生成。

AIにFFmpeg処理を任せず、同じSVGから同じMP4を再生成できるようにする。

Paper → Skill → AW → Render WF → MP4 Artifact
