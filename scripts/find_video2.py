import json
import re
import os

c = open(os.path.join(os.environ["TEMP"], "woodowel.html"), encoding="utf-8", errors="ignore").read()

for script_id in ["wix-viewer-model", "wix-warmup-data", "wix-essential-viewer-model"]:
    m = re.search(rf'id="{script_id}">(.+?)</script>', c, re.DOTALL)
    if not m:
        continue
    text = m.group(1)
    if "lygha6r9" in text:
        print(f"Found lygha6r9 in {script_id}")
        idx = text.find("lygha6r9")
        print(text[max(0, idx - 300) : idx + 2000][:1500])
        print()

# search video file refs
for pat in [
    r"video_[a-f0-9]+",
    r"007d85_[a-f0-9]+~mv2\.mp4",
    r"d838ea_[a-f0-9]+~mv2\.mp4",
    r'"videoRef"[^}]{0,400}',
    r'"videoData"[^}]{0,800}',
]:
    hits = set(re.findall(pat, c))
    if hits:
        print("PAT", pat, "count", len(hits))
        for h in list(hits)[:5]:
            print(h[:500])
        print()
