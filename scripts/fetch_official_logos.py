import re
import urllib.request

html = urllib.request.urlopen(
    urllib.request.Request("https://www.uvic.ca/", headers={"User-Agent": "Mozilla/5.0"}),
    timeout=20,
).read().decode("utf-8", errors="ignore")
for m in re.findall(r'(?:src|data-src)="([^"]+\.(?:png|jpg|svg)[^"]*)"', html, re.I):
    if "uvic" in m.lower() or "logo" in m.lower() or "brand" in m.lower():
        print(m)
