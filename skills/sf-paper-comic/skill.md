# SF Paper Comic Skill

## Purpose
論文の研究上の発見を、SF四コマ→SVGアニメ→YouTube用素材へ変換する再利用可能スキル。

## Input
- P番号
- paper README / metadata
- 研究への取り込み方

## Workflow
1. 論文の事実と演出を分離する。
2. 「問題→異変→発明→オチ」の4コマ脚本を作る。
3. 各コマをSVG storyboardとして生成する。
4. ①→②→③→④を時間軸アニメーションにする。
5. narration / SFX / timing metadataを生成する。
6. YouTube 45–90秒のepisode packageにする。

## Rules
- 論文の実験結果を創作しない。
- SF設定・キャラクター・台詞は演出層。
- 最後は必ずhw-sotsuseiの研究ループへ接続する。
- 論文SVGと漫画SVGは別物として保持する。
- 1論文 = 1エピソード。
- purple-only visual languageを基本とする。

## Output
`papers/youtube/comics/Pxx.svg`
`papers/youtube/episodes.jsonl`

## Episode schema
`id, title, hook, panels[4], research_connection, duration, narration, sfx`

## Quality gate
- 4コマだけで研究の核心が分かる
- 論文の事実と創作を区別できる
- 研究ループへの接続がある
- 60–90秒へ展開可能
