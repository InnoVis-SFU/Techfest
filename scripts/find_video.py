import json
import re
import os

c = open(os.path.join(os.environ["TEMP"], "woodowel.html"), encoding="utf-8", errors="ignore").read()
m = re.search(r'id="wix-viewer-model">(.+?)</script>', c, re.DOTALL)
data = json.loads(m.group(1))
found = []


def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            kl = k.lower()
            if any(x in kl for x in ["video", "mp4", "poster", "qualities"]) or k in (
                "uri",
                "url",
                "videoUrl",
            ):
                found.append((f"{path}.{k}", v))
            walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{path}[{i}]")


walk(data)
for p, v in found:
    s = json.dumps(v) if not isinstance(v, str) else v
    if any(x in s.lower() for x in ["mp4", "video", "007d85", "d838ea", "youtube"]):
        print(p, ":", s[:400])
        print()
