#!/usr/bin/env python3
import os
import re
import sys
import urllib.request

path = sys.argv[1] if len(sys.argv) > 1 else "about-1-1"
url = f"https://www.codesignexplore.com/{path}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
page = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", errors="ignore")

links = [
    l.replace("\\/", "/")
    for l in re.findall(
        r"https://siteassets\.parastorage\.com/pages/pages/thunderbolt[^\"'\\]+",
        page,
    )
]
feat = [l for l in links if "module=thunderbolt-features" in l]
link = feat[0] if feat else links[0]
print("Using", link[link.find("pageId="):link.find("&piler")], "...")

data = urllib.request.urlopen(link, timeout=60).read().decode("utf-8", errors="ignore")
out = os.path.join(os.environ["TEMP"], f"tb-{path}.json")
open(out, "w", encoding="utf-8").write(data)
print("len", len(data))

for m in re.finditer(
    r'"src":"(https://(?:www\.)?(?:youtube\.com/watch\?v=[^"]+|youtu\.be/[^"]+))"',
    data,
):
    print("VIDEO", m.group(1))

idx = 0
while True:
    idx = data.find('"fullNameCompType":"wixui.ImageX"', idx)
    if idx == -1:
        break
    start = data.rfind('"comp-', idx - 80, idx)
    cid_m = re.match(r'"(comp-[^"]+)"', data[start:])
    chunk = data[start : start + 2000]
    uris = re.findall(r'"uri":"([^"]+~mv2\.[^"]+)"', chunk)
    if cid_m and uris:
        print("IMG", cid_m.group(1), uris[0])
    idx += 1

for m in re.finditer(r'"componentType":"VideoPlayer"', data):
    chunk = data[m.start() : m.start() + 800]
    print("VP", chunk[:400])
