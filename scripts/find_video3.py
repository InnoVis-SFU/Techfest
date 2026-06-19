import json
import re
import os

c = open(os.path.join(os.environ["TEMP"], "woodowel.html"), encoding="utf-8", errors="ignore").read()
m = re.search(r'id="wix-viewer-model">(.+?)</script>', c, re.DOTALL)
data = json.loads(m.group(1))
text = json.dumps(data)

for term in ["lygha6r9", "lygh2qxw", "VideoPlayer", "videoData", "007d85_35da", "qualities"]:
    if term in text:
        print(term, "FOUND")
        for match in re.finditer(re.escape(term), text):
            print(text[max(0, match.start() - 100) : match.start() + 400])
            print("---")
            break

# save compact search
idx = text.find("lygha6r9")
if idx == -1:
    # search nested structure for components
    def find_key(o, target):
        if isinstance(o, dict):
            if target in o:
                return o[target]
            for v in o.values():
                r = find_key(v, target)
                if r is not None:
                    return r
        elif isinstance(o, list):
            for v in o:
                r = find_key(v, target)
                if r is not None:
                    return r
        return None

    r = find_key(data, "comp-lygha6r9")
    print("comp-lygha6r9 data:", json.dumps(r, indent=2)[:2000] if r else None)
