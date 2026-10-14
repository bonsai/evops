#!/usr/bin/env python3
"""
Kaggle GPU Evaluation Script
Runs inside Docker container with GPU support.
Evaluates PNG images using CLIP semantic similarity.
"""
import os
import json
import glob
import sys
from pathlib import Path

# Install dependencies
os.system("pip install -q clip torch ftfy regex tqdm")

import torch
import clip
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")
if device == "cuda":
    print(f"GPU: {torch.cuda.get_device_name(0)}")

INPUT_DIR = "/workspace/inputs"
OUTPUT_DIR = "/workspace/results"

# Create output directory
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# Load CLIP model
print("Loading CLIP model...")
model, preprocess = clip.load("ViT-B/32", device=device)
print("CLIP model loaded.")

# Define evaluation prompts
PROMPTS = [
    "a cute chubby penguin character with pink cap",
    "a thin Spanish knight with a lance",
    "a blue robotic cat with a round body",
    "a 4-panel manga illustration with speech bubbles",
]


def evaluate_image(image_path: str, prompt: str) -> float:
    """Evaluate image against a prompt using CLIP."""
    try:
        image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
        text = clip.tokenize([prompt]).to(device)
        with torch.no_grad():
            logits_per_image, _ = model(image, text)
            score = float(logits_per_image[0][0])
        return score
    except Exception as e:
        print(f"Error evaluating {image_path}: {e}")
        return 0.0


def evaluate_all():
    """Evaluate all PNG images in input directory."""
    image_paths = []
    for ext in ["*.png", "*.jpg", "*.jpeg"]:
        image_paths.extend(glob.glob(os.path.join(INPUT_DIR, "**", ext), recursive=True))
    
    if not image_paths:
        print(f"No images found in {INPUT_DIR}")
        return {}
    
    print(f"Found {len(image_paths)} images to evaluate")
    
    results = {}
    for path in image_paths:
        filename = os.path.basename(path)
        print(f"Evaluating {filename}...")
        
        scores = {}
        for prompt in PROMPTS:
            score = evaluate_image(path, prompt)
            scores[prompt] = round(score, 4)
        
        # Use best score as the evaluation score
        best_score = max(scores.values())
        results[filename] = {
            "best_score": best_score,
            "scores": scores,
            "path": path,
        }
        print(f"  {filename}: best={best_score:.4f}")
    
    # Save results
    output_path = os.path.join(OUTPUT_DIR, "eval_result.json")
    with open(output_path, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nResults saved to {output_path}")
    print(f"Total images evaluated: {len(results)}")
    return results


if __name__ == "__main__":
    evaluate_all()