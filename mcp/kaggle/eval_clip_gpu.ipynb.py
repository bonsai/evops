"""
Kaggle Notebook: evops GPU Evaluation
Requires: GPU runtime (P100/T4)
"""

# Install dependencies
!pip install -q ftfy regex tqdm
!pip install -q git+https://github.com/openai/CLIP.git

import torch, clip, json, os, glob
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Update this path to Kaggle input
IMAGE_DIR = "/kaggle/input/evops-images"
OUTPUT_JSON = "/kaggle/working/eval_result.json"

prompt = "a 4-panel manga illustration with speech bubbles"

def evaluate_image(path: str) -> dict:
    image = preprocess(Image.open(path)).unsqueeze(0).to(device)
    text = clip.tokenize([prompt]).to(device)
    with torch.no_grad():
        logits_per_image, _ = model(image, text)
        score = float(logits_per_image[0][0]) / 100.0
    return {"clip_score": round(score, 4), "path": path}

results = {}
for path in glob.glob(os.path.join(IMAGE_DIR, "*.png")) + glob.glob(os.path.join(IMAGE_DIR, "*.jpg")):
    results[os.path.basename(path)] = evaluate_image(path)

with open(OUTPUT_JSON, "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("GPU evaluation done:", len(results), "images")
print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU mode")
