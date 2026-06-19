import json
import re
import os

data = open(os.path.join(os.environ["TEMP"], "thunderbolt.json"), encoding="utf-8").read()

# find video player config
for m in re.finditer(r"comp-lygha6r9", data):
    chunk = data[m.start() : m.start() + 3000]
    if "video" in chunk.lower() or "mp4" in chunk.lower() or "uri" in chunk:
        print(chunk[:2500])
        print("\n=====\n")

# search mp4
for u in sorted(set(re.findall(r"https://video\.wixstatic\.com/[^\"\\]+", data))):
    print("VIDEO", u)

for u in sorted(set(re.findall(r"[a-f0-9]{8}_[a-f0-9]+~mv2\.mp4", data))):
    print("MP4 ID", u)

for cid in ["comp-lygh2qxw", "comp-lyghcd84", "comp-lyghsl5w", "comp-lyghokp8"]:
    m = re.search(rf'"{cid}":\{{.*?"imageData":\{{"uri":"([^"]+)"', data)
    print(cid, m.group(1) if m else "not found")

try:
    j = json.loads(data)
    text = json.dumps(j)

    def find_comp(o, comp_id):
        if isinstance(o, dict):
            if o.get("id") == comp_id or o.get("componentId") == comp_id:
                return o
            for v in o.values():
                r = find_comp(v, comp_id)
                if r:
                    return r
        elif isinstance(o, list):
            for v in o:
                r = find_comp(v, comp_id)
                if r:
                    return r
        return None

    comp = find_comp(j, "comp-lygha6r9")
    if comp:
        print("COMP DATA:", json.dumps(comp, indent=2)[:4000])
except json.JSONDecodeError as e:
    print("not pure json", e)
