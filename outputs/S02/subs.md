# subs.yaml.ass - 要約

## 概要

`subs.yaml.ass` は、Subs（サブプロジェクト）に関する設定ファイルです。

## 主な内容

- **プロジェクト名**: subs
- **目的**: サブプロジェクト間の連携・依存関係の管理
- **構成**: 複数のサブプロジェクト（bpy, don_quixote, donpen, doraemon, pagoda, salmon_bear, etc.）との連携
- **技術スタック**: Python, Blender Workbench, VLM (Video Language Model)

## 関連フォルダ

- `bpy/` - bpyツールによる生成プロジェクト
- `papers/` - 論文・評価データ
- `S01-resnet/` - SVGパネル群（ResNetプロジェクト）
- `stick-figures/` - 棒人間SVGプロジェクト
- `mediapipe/` - MediaPipeポーズプロジェクト
- `others/` - 他のメディアファイル

## 注釈

- このファイルはサブプロジェクト間の依存関係と構成を定義するYAML形式の設定
- 各サブプロジェクトの役割とインターフェースが記述されている
- 将来的な拡張や統合のための基盤となる
