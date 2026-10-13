import numpy as np
from PIL import Image

STAR_SIZE = 2048
path = r"C:\Users\0501JP\sotsusei\project\eggs\egg-shadow\blender\starfield.png"
star_img = Image.new("RGB", (STAR_SIZE, STAR_SIZE // 2), (0, 0, 0))
px = star_img.load()
np.random.seed(42)
n_stars = STAR_SIZE // 2
for _ in range(n_stars):
    x, y = np.random.randint(0, STAR_SIZE), np.random.randint(0, STAR_SIZE // 2)
    s = np.random.randint(1, 3)
    b = int(np.random.uniform(0.3, 1.0) * 255)
    color = (b, b, b)
    for dx in range(-s, s + 1):
        for dy in range(-s, s + 1):
            xx, yy = x + dx, y + dy
            if 0 <= xx < STAR_SIZE and 0 <= yy < STAR_SIZE // 2:
                px[xx, yy] = color
star_img.save(path, quality=95)
print("starfield:", path)
