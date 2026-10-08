# SF Paper Comic MCP

論文をSF四コマYouTubeエピソードへ変換するMCP。

## Tool
- `make_episode` — P番号、タイトル、4コマ脚本からepisode JSONを作る
- `make_timeline` — 45–90秒の4コマ時間配分を作る

## Role
MCP = act / orchestration tool。
論文知識そのものは `skills/sf-paper-comic` に置き、MCPは脚本・タイムライン生成を実行する。

## Loop
Paper Skill → MCP episode → SVG → narration/SFX → YouTube
