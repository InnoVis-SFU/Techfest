import re
import html
import os

path = os.path.join(os.environ["TEMP"], "woodowel.html")
with open(path, encoding="utf-8", errors="ignore") as f:
    c = f.read()

for pat in [
    r"https://video\.wixstatic\.com/[^\"\\]+",
    r"https://www\.youtube\.com/[^\"\\]+",
    r"https://youtu\.be/[^\"\\]+",
    r"videoUrl[^\"]{0,200}",
    r"\"videoId\"[^,]{0,120}",
    r"wixstatic\.com/media/007d85[^\"\\]+",
    r"wixstatic\.com/media/d838ea[^\"\\]+",
]:
    matches = set(re.findall(pat, c))
    if matches:
        print(f"=== {pat[:40]} ===")
        for m in sorted(matches)[:15]:
            print(html.unescape(m)[:200])
        print()
