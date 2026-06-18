import re, html, os
c = open(os.environ["TEMP"] + "/codesign.html", encoding="utf-8", errors="ignore").read()
seen = set()
for m in re.finditer(r'href="(https://www\.codesignexplore\.com/about[^"]*)"', c):
    url = m.group(1)
    if url in seen:
        continue
    seen.add(url)
    start = max(0, m.start() - 600)
    chunk = c[start : m.end() + 80]
    t = re.sub(r"<[^>]+>", " ", chunk)
    t = html.unescape(re.sub(r"\s+", " ", t)).strip()
    print(url)
    print(" ", t[-250:])
    print()
