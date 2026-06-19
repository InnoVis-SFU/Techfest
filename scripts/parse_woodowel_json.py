import json
import re
import os

path = os.path.join(os.environ["TEMP"], "woodowel.html")
with open(path, encoding="utf-8", errors="ignore") as f:
    c = f.read()

m = re.search(r'id="wix-viewer-model">(.+?)</script>', c, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    # dump keys related to video
    text = json.dumps(data)
    for key in ["lygha6r9", "lygh2qxw", "lyghcd84", "lyghsl5w", "lyghokp8", "video", "mp4", "VideoPlayer"]:
        if key.lower() in text.lower():
            pass
    # find all mp4 and video urls
    for u in sorted(set(re.findall(r"https?:\\\/\\\/[^\"\\]+", text))):
        u = u.replace("\\/", "/")
        if any(x in u.lower() for x in ["mp4", "video", "youtube", "wixstatic.com/media"]):
            if "parastorage" not in u or "media" in u:
                print(u[:250])

# also warmup data
m2 = re.search(r'id="wix-warmup-data">(.+?)</script>', c, re.DOTALL)
if m2:
    w = json.loads(m2.group(1))
    print("\n--- warmup ---")
    print(json.dumps(w.get("pages", {}), indent=2)[:4000])
