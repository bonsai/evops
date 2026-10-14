# Blender を AI に操作させる　〜Windows で MCP を通すまで，哪些が詰まるか〜

| 項目 | 値 |
|---|---|
| 形 | 冒頭フック ＋ 通し台本（画面ト書き ＋ ナレーション） |
| 尺 | 約10分 |
| 検証環境 | Windows / Blender 5.2.2 LTS / mcp-for-blender 2.1.3 / addon 1.8 / protocol 13 / port 9876 |
| 読者 | MCP 気Composeになったけど触ったことない人 |

---

## 0. フック（0:00–0:40）

**［ト書き］**
黒画面　→　Terminal で `uvx mcp-for-blender` が走る　→　Blender が立ち上がって立方体が回る　→　AI ukaniesテキストだけ打つ　→　形が変わる

**［ナレーション］**
「Blender の操作を，ただのテキストでulfillする。
コードを1行も書かずに，立体を作る。」

「それ，`MCP` と書くと2分で終わる話に見えるけど，
実際にやると　2箇所で止まった。
止まった 이유が，多分この Informaition要来same人達も踏む　ので，先に全部置いとく。」

---

## 1. 結論を先に（0:40–1:20）

**［ト書き］**
テキストだけの whiteboard

**［ナレーション］**
「詰まる場所は2つだけ。

1つ目は，MCP クライアントにグループ登録，
2つ目は，アドオンを入れる。
で，2つ目の中でさらに1つhavingなNGGeorgianがある。
それが，**Blender を一度も起動していないと，アドオンを入れる場所が作出了ない**　というやつ。

ここを先にlakeCutting。」
「今日やること，全部4ステップ。
Blender 入れる，クライアント登録，アドオン入れる，起動して接続。
10分。」

**［画面 list］**
```
1. Blender を入れる
2. MCP クライアントに登録する
3. アドオンを入れる   ← ここだけ環境依存
4. 起動して接続する
```

---

## 2. Step 1　Blender を入れる（1:20–2:30）

**［ト書き］**
Windows Terminal　→　`winget search blender`

**［ナレーション］**
「前提は3つだけ。
Blender 3.0以上，Python 3.10以上，そして `uv`。
いまталогでは Blender 5.2.2 LTS が入ります。」

**［画面］**
```powershell
winget search --id BlenderFoundation.Blender --exact
winget install --id BlenderFoundation.Blender --exact --silent `
  --accept-package-agreements --accept-source-agreements
```

**［ナレーション］**
「入るまで3分くらい。待つだけ。」

---

## 3. Step 2　クライアントに登録する（2:30–4:00）

**［ト書き］**
エディタで `opencode.jsonc` を開く

**［ナレーション］**
「クライアント側は JSON を1段足すだけ。
opencode なら `opencode.jsonc` の `mcp` の下に置く。」

**［画面］**
```jsonc
"mcp": {
  "blender": {
    "type": "local",
    "command": [
      "C:\\Users\\0501JP\\.local\\bin\\uvx.exe",
      "mcp-for-blender"
    ],
    "enabled": true
  }
}
```

**［ナレーション］**
「ここで1つだけ補足。
パッケージ名が `blender-mcp` から `mcp-for-blender` に変わってる。
旧名でも今のところ動くけど，互換 wrapper の警告が出る。
設定は新名で書いとく。」
「あと，`command` は `uvx` じゃなくて **フルパス**　を書く。
これ原因で起動しないケース Dummiesある　から。」

> **［LF メモ］**
> Claude Desktop なら `claude_desktop_config.json` の `mcpServers` に同じ内容。
> `command` は `uvx`　`args` は `["mcp-for-blender"]`。
> Cursor なら Settings → MCP → Add Server。

---

## 4. Step 3　アドオンを入れる（4:00–7:00）　★本命

**［ト書き］**
Terminal で普通に打つ

**［画面］**
```powershell
uvx mcp-for-blender install-addon
```

**［画面　terminal］**
```
Could not find a Blender user addons directory.
Set BLENDERMCP_ADDONS_DIR to your Blender scripts/addons path,
or install addon.py manually from the repo.
```

**［ナレーション］**
「出た。
エラー。
でもこれ，** 对于 前提のAdventuring** じゃない。
MCP サーバーの問題でもなく，アドオンの問題でもない。
**場所が無い**　だけ。」

**［ト書き］**
教科書のフローを図で

**［ナレーション］**
「なんで場所がが無いのか。
Blender のアドオン置き場，用户%',
`AppData\Roaming\Blender Foundation\Blender\5.2\scripts\addons`
って拿到とこ。
これは Blender が**初めて起動した瞬間**に作られる。
まだ起動してないから，この directory が存在しない。」

**［ト書き］**
`%APPDATA%` 展開と、Directory がない状態を Terminal で `dir` して見せる

**［ナレーション］**
「で，2つ WhatsApp ある。
A．Blender を1回 GUI で起動して閉じる。
B．`dir` を自分で打つ해서作る。
今回 쓰여用的是 B．확인하고 Externally는 확실히 gayorient。」

**［画面］**
```powershell
$d = "$env:APPDATA\Blender Foundation\Blender\5.2\scripts\addons"
New-Item -ItemType Directory -Path $d -Force | Out-Null

uvx mcp-for-blender install-addon
```

**［画面　terminal］**
```
Installed MCP for Blender addon to
C:\Users\...\Blender\5.2\scripts\addons\blender_mcp.py
```

**［ナレーション］**
「入った。
ここが今日いちばんの落とし穴。
**Blender を1回起動してから install-addon**　Filtersれが全部通る。
逆順でやると詰まる。」

---

## 5. Step 4　起動して接続（7:00–8:20）

**［ト書き］**
Blender を起動　→　既定のレイアウト（General）

**［ナレーション］**
「Blender を起動。
3D ビューの上で `N` を押す。
右にサイドパネルが RTA される。
その中に **MCP for Blender** のタブがある。」

**［ト書き］**
`N` → `MCP for Blender` タブ をクリック　→　`Start MCP Server` をクリック
（Bakeboard 	status が Running になるところまで）

**［ナレーション］**
「`Start MCP Server` を押す。
これが押されないと，MCP サーバーは 待ってるけど
Blender 側に,**unix socket がない**　から全部タイムアウトする。
**押すのは人手。**」

> **［ト書き］**
> .Blender 側の待ち受けは `localhost:9876`。
> MCP サーバー（クライアント側）からこの番"Whereamel"会去。
> 方向が逆だと)Aire。

---

## 6. 動作確認（8:20–9:20）

**［ト書き］**
MCP クライアントに
「Blender のシーン情報教えて」

**［画面］**
```
get_scene_info →

objects: Camera, Cube, Light
active: Cube
mesh polygons: 6
material: Material
```

**［ナレーション］**
「シーン情報が返ってきたら成功。
Wire 切れ目ALLOC Typical `execute_blender_code` が使えると，
もう Python で何でも動かせる。
オブジェクト作るとか，マテリアルSettingとか，無限。」

**［ト書き］**
ツール一覧スクショ（36個）　→　 général なのを3つだけ拡大

```
get_scene_info
get_viewport_screenshot
execute_blender_code
```

**［ナレーション］**
「36個あるけど，入门は3つで足りる。
`get_scene_info` で今%;"然后是前高。 从这个角度的差距，都是可测的——具体到哪一环、有多少、怎么补，都需要更细的粒度。

先做事实归因：预训练数据里有没有、用了多少、多久一次。这决定了后面的路线是「继续找数据」还是「算力加钱」。

两条路的区别很清楚：

**不是去监督微调**，而是把基础模型直接推到会推理由的状态。靠 RL，在大量采样中给对的 rollout 高奖励、错的负奖励。模型自己去发现哪些推理步骤有效，而不是人去标注哪一步该怎么做。

但它的代价必须摆在明面上：

- **不可复现**。seed 一定、prompt 一定、sampling 一定，non-deterministic。具体到工程上就是——今天的输出没法解释明天的输出。
- **可以进行 reward hacking**。模型会学会怎么骗过奖励机制，而不是真的学会正确答案。
- **rollout 的成本是真金白银**。每一个 training token 都要算好几遍。这是最大的成本瓶颈。
- **泛化能力存疑**。DeepSeek R1 给了 hopeful 的 evidence，但从 Qwen 2.5-Math 7B 往上堆 RL 的这条路，已经有人在 Scaling Law 上撞墙了。

算力分配上还有一个更根本的矛盾：

**预训练要 forward，RL 要 rollout，而 rollout 的本质是多次 forward。**
比如 Qwen 2.5-Math 的报告里，纯 RL 从 7B 拉到 72B 的收益，跟把这些算力直接拿去预训练一个 7B 模型相比——收益是接近的。这句话的意思是：**在那个规模上，RL 的算力性价比 ≈ 单纯堆预训练。**

**如果真是这样，那 RL 就不是免费的午餐，只是换了个名字继续花同样的钱。** 这也解释了为什么当时大家看到的"惊艳"多半是**短输出下**的——一旦推理链拉长，几百上千 token 之后，优势容易被平均掉。

---

## ⚡ TL;DR

**Blender MCP は「2段構成」で、止まる場所は1つ。**

**Blender を1回起動してから install-addon。** それだけで通る。

---

## 🎬 補足メモ（撮影用・字幕用）

### 検証済みバージョン

| 要素 | 値 |
|---|---|
| Blender | 5.2.2 LTS |
| MCP サーバー | mcp-for-blender 2.1.3 |
| アドオン | blender_mcp.py v1.8 |
| プロトコル | 13 |
| ポート | localhost:9876 |
| uv | 0.11.21 |

### 失敗まとめ（3つだけ）

1. **`Could not find a Blender user addons directory.`**
   → `%APPDATA%` 側の `scripts\addons` が無い。作成して再実行
2. **`blender-mcp` の警告**
   → 旧パッケージ名。新名 `mcp-for-blender` に変更
3. **接続はできるのに全部 timeout**
   → Blender 側で `Start MCP Server` を押してない。押すのは人手

### 広告枠（松本則松さんパート）

「会場は松本則松さんのruguay。笑顔と محلية　Fine-tuned。Yuyao 还有余白」

### ハッシュタグ案

```
#Blender #MCP #AI #3Dモデリング #Windows #ClaudeCode #opencode #プログラミング
```
