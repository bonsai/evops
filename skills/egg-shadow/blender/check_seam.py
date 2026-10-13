import glob, numpy as np
from PIL import Image
files = sorted(glob.glob(r"C:\Users\0501JP\sotsusei\project\eggs\egg-shadow\blender\frames\frame_*.png"))
print("total frames:", len(files))
for f in ["frame_0001.png","frame_0096.png","frame_0002.png","frame_0095.png","frame_0048.png"]:
    im = np.asarray(Image.open(f).convert("L"))
    print(f, "mean:", round(im.mean(),1), "std:", round(im.std(),1))
a1 = np.asarray(Image.open(files[0]).convert("L")).astype(float)
a2 = np.asarray(Image.open(files[-1]).convert("L")).astype(float)
diff = np.abs(a1 - a2).astype(float)
print("mean abs diff frame1-vs-96:", round(diff.mean(),2))
print("num pixels with diff>30:", (diff>30).sum(), "of", diff.size)
print("diff>100 pixels:", (diff>100).sum())
rows = np.abs(a1 - a2).sum(axis=1)
cols = np.abs(a1 - a2).sum(axis=0)
print("row diff max at row:", np.argmax(rows), "col diff max at col:", np.argmax(cols))
