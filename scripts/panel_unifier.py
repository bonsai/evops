#!/usr/bin/env python3
"""
Merge panel images with generation numbers using paper-id prefixing.
Usage:
    python3 scripts/panel_unifier.py --paper-id S01 --output /home/bons/evops/outputs/papers/S01/
"""
import argparse
import shutil
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Merge panels with generation numbers')
    parser.add_argument('--paper-id', type=str, required=True, help='Paper ID (e.g., S01)')
    parser.add_argument('--output', type=Path, required=True, help='Output directory')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without copying')
    
    args = parser.parse_args()
    
    output_dir = args.output
    paper_id = args.paper_id
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all panel files (SVG, PNG, etc.)
    panel_files = []
    for path in Path('/home/bons/evops/outputs').rglob('*'):
        if path.suffix in ['.svg', '.png', '.jpg', '.jpeg']:
            filename = path.name
            # Extract paper ID from filename (e.g., S01_panel_01.svg → S01)
            parts = filename.split('_')
            if len(parts) >= 2:
                pid = parts[0]
                # Extract panel index (e.g., S01_panel_01.svg → 01)
                panel_index_str = parts[-1].split('.')[0]
                if panel_index_str.isdigit():
                    panel_index = int(panel_index_str)
                    panel_files.append({
                        'path': path,
                        'paper_id': pid,
                        'index': panel_index,
                    })
    
    # Find all PNG images
    png_files = []
    for png_file in Path('/home/bons/evops/outputs').rglob('*.png'):
        name = png_file.name
        # Extract generation index (e.g., gen_donpen_00.png → 00)
        parts = name.split('_')
        gen_index_str = parts[-1].split('.')[0]
        if gen_index_str.isdigit():
            gen_index = int(gen_index_str)
            png_files.append({
                'path': png_file,
                'generation_index': gen_index,
                'basename': name,
            })
    
    # Match panels with generation images by index
    matched_pairs = []
    for panel in panel_files:
        for png in png_files:
            if panel['index'] == png['generation_index']:
                matched_pairs.append({
                    'paper_id': paper_id,
                    'panel_index': panel['index'],
                    'panel_path': panel['path'],
                    'panel_name': panel['path'].name,
                    'generation_index': png['generation_index'],
                    'png_path': png['path'],
                    'png_name': png['basename']
                })
    
    # Copy PNGs with new naming convention
    for pair in matched_pairs:
        new_name = f"{paper_id}_panel_{pair['generation_index']}.png"
        new_path = output_dir / new_name
        
        if args.dry_run:
            print(f"[DRY RUN] Would copy {pair['panel_path']} → {new_path}")
        else:
            shutil.copy2(pair['panel_path'], new_path)
            print(f"✅ Copied {pair['panel_path'].name} → {new_name}")
    
    print(f"✅ Processed {len(panel_files)} panel files")

if __name__ == "__main__":
    main()