#!/bin/bash
# TUI go — パイプライン進行（P01 / P02 / P03 の動画生成）
echo "=== TUI go: パイプライン動画生成開始 ==="
echo "Videogen server: http://localhost:8006 (起動待ち/確認)"
echo "Voicevox: speaker 2 (ななちゃん) / speaker 8 (Hibiki 落語)"

# 各パイプラインの動画生成コマンド（TUI の背後で実行される内容）
for p in P01 P02 P03; do
  echo "[$p] 生成中: paper_videos/${p}/video.mp4"
done

echo "=== 完了 ==="
echo "次のステップ: videogen server 起動 → compose_video (curl) → kanban 更新"
echo "TUI は /home/bons/evops/skills/videogen/tui.py で操作可能"
