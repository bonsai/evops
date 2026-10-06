# 画像生成パイプライン：Blender + bpy + SVG

## 背景

- **ComfyUI / ローカルモデル**: ハードウェア・モデル管理・環境構築が重い。
- **Web API**: 無料枠もあるが API key 管理、課金、外部依存が煩わしい。
- **結論**: まず **Blender + bpy + SVG** で自分の手元で完結するパイプラインを作る。

## アプローチ

```text
[SVG 作成] → [Blender 読み込み] → [3D 化 / マテリアル / ライティング] → [レンダリング] → [画像]
```

### 1. SVG 作成

- 手描き or コード生成（Python: `svgwrite`, `svgpathtools` など）
- ベースとなる線画、シルエット、カラーパレットを定義

### 2. Blender 読み込み

```python
import bpy

# SVG インポート
bpy.ops.import_curve.svg(filepath="path/to/image.svg")
```

### 3. 3D 化・表現

- カーブからメッシュ化（`bpy.ops.object.convert(target='MESH')`）
- ソリッド化（Solidify モディファイア）
- マテリアル・ライティング・カメラ設定

### 4. レンダリング

```python
bpy.context.scene.render.filepath = "path/to/output.png"
bpy.ops.render.render(write_still=True)
```

## 応用：自動生成ループ

```text
[パラメータ生成] → [SVG 生成] → [Blender レンダリング] → [評価] → [次のパラメータに反映]
```

- SVG 生成パラメータ: 形、色、配置、線の太さなどを数値化
- パラメータ空間を探索し、評価の高い方向へ反復

## 利点

- 外部 API key が不要
- 再現性が高い（SVG + パラメータで完全再現可能）
- 3D 表現・レンダリングを組み合わせた豊かなビジュアルが作れる
- ポートフォリオとしても見せやすい

## 課題

- 作業用 PC の GPU/CPU パワー
- 複雑な絵柄は SVG 化が大変
- 写実的な生成は苦手（スタイル化されたビジュアル向き）

## カイカイキキとの親和性

- 村上隆スタイルの「フラットでポップ、SVG に適した図形的表現」
- カラーパレットやキャラクター構造をパラメータ化しやすい
- アニメーション / 立体作品への展開も可能

## 次のアクション

- [ ] Blender で SVG → レンダリングの最小スクリプトを作成
- [ ] SVG パラメータを JSON or YAML で定義できるようにする
- [ ] 複数パターンを一括レンダリングするバッチ処理を作る
