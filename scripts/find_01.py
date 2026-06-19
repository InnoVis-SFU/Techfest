#!/usr/bin/env python3
import re
import html
import urllib.request

page = urllib.request.urlopen("https://www.codesignexplore.com", timeout=60).read().decode("utf-8", errors="ignore")
m = re.search(r"\{01\}[\s\S]{0,3000}?href=\"(https://www\.codesignexplore\.com/about[^\"]+)\"", page)
if m:
    print("01 URL", m.group(1))
    chunk = m.group(0)
    text = html.unescape(re.sub(r"<[^>]+>", " ", chunk))
    print(re.sub(r"\s+", " ", text)[:200])
