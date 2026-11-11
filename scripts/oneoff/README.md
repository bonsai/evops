# scripts/oneoff/ — 一回限りのパッチ

`custom-skills/tmp` から巻き取ったもの（2026-11-10）。

| ファイル | 中身 |
|---|---|
| `fix2b.py` | `evops/docs/40-submit/split/part02_deliver.html` の表 4 行を差し替える使い捨てパッチ |

## 注意

- 対象パスは WSL（`/home/bons/evops/...`）前提。今の環境には無いので**再実行しないこと**。
- 同じ修正をやり直すときは、置換前後の HTML を行単位で確認してから当てる。
