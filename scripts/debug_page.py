#!/usr/bin/env python3
import re
import sys
import urllib.request

path = sys.argv[1] if len(sys.argv) > 1 else "about-1"
url = f"https://www.codesignexplore.com/{path}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
page = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", errors="ignore")

# page ids
for pat in [
    r'"pageId":"([^"]+)"',
    r'"pageUriSEO":"' + re.escape(path) + r'"[^}]*"id":"([^"]+)"',
    r'wixstatic\.com/media/([a-f0-9_~mv2\.a-z]+)',
]:
    matches = re.findall(pat, page)
    print(f"=== {pat[:50]} ===")
    for m in sorted(set(matches))[:20]:
        print(" ", m)

links = re.findall(
    r"https://siteassets\.parastorage\.com/pages/pages/thunderbolt[^\"'\\]+",
    page,
)
print("\nthunderbolt URLs:")
for link in links:
    print(link.replace("\\/", "/"))


# static images on page
imgs = []
for m in re.finditer(r"wixstatic\.com/media/([a-f0-9_]+~mv2\.[a-z]+)", page):
    if m.group(1) not in imgs:
        imgs.append(m.group(1))
print(f"\nstatic images ({len(imgs)}):")
for i in imgs[:15]:
    print(" ", i)
