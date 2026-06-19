#!/usr/bin/env python3
import re
import html
import urllib.request

page = urllib.request.urlopen("https://www.codesignexplore.com", timeout=60).read().decode("utf-8", errors="ignore")

# project cards use {01} etc
blocks = re.findall(
    r"\{(\d{2})\}[\s\S]{0,2500}?href=\"(https://www\.codesignexplore\.com/about[^\"]+)\"",
    page,
)
for num, url in blocks:
    path = url.split("/")[-1]
    chunk_m = re.search(rf"\{{{num}\}}[\s\S]{{0,2500}}?href=\"{re.escape(url)}\"", page)
    chunk = chunk_m.group(0) if chunk_m else ""
    text = html.unescape(re.sub(r"<[^>]+>", " ", chunk))
    text = re.sub(r"\s+", " ", text).strip()
    # title after number
    title_m = re.search(rf"\{{{num}\}}\s*(.+?)(?:Explore this project|Project members|\{{)", text)
    title = title_m.group(1).strip()[:70] if title_m else text[:70]
    print(f"{num} {path:22s} {title}")
