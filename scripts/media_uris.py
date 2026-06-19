import os
import re

data = open(os.path.join(os.environ["TEMP"], "thunderbolt.json"), encoding="utf-8").read()

for cid in ["comp-lygh2qxw", "comp-lyghcd84", "comp-lyghsl5w", "comp-lyghokp8"]:
    idx = data.find(f'"{cid}":{{"fullNameCompType"')
    if idx == -1:
        idx = data.find(f'"{cid}":{{"componentType"')
    chunk = data[idx : idx + 1200]
    uris = re.findall(r'"uri":"([^"]+)"', chunk)
    print(cid, uris)
