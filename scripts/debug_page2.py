#!/usr/bin/env python3
import re
import sys
import urllib.request

path = sys.argv[1]
url = f"https://www.codesignexplore.com/{path}"
page = urllib.request.urlopen(
    urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
    timeout=60,
).read().decode("utf-8", errors="ignore")

for term in ["warmupData", "pagesMap", "pageUriSEO", "VideoPlayer", "lygha6r9", "viewerModel", "siteAssets"]:
    if term in page:
        print(f"found {term}")

# page uri mapping
for m in re.finditer(r'"pageUriSEO":"([^"]+)"[^}]{0,200}"pageId":"([^"]+)"', page):
    print("URI", m.group(1), "->", m.group(2))

for m in re.finditer(r'"pageUriSEO":"([^"]+)"', page):
    uri = m.group(1)
    if path in uri or uri.startswith("about"):
        start = m.start()
        print("chunk", page[start:start+300])

# try alternate pattern
for m in re.finditer(rf'"pageUriSEO":"{re.escape(path)}"', page):
    chunk = page[m.start()-200:m.start()+500]
    print("MATCH", chunk)
