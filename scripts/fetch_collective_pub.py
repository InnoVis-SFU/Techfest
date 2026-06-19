import json
import re
import urllib.request

url = "https://www.codesignexplore.com/about-1-2-1-1-2-1"
page = urllib.request.urlopen(url, timeout=60).read().decode("utf-8", errors="ignore")

# button link near Read the Publication
idx = page.find("Read the Publication")
if idx != -1:
    chunk = page[max(0, idx - 1500) : idx + 500]
    for m in re.finditer(r'href="(https?://[^"]+)"', chunk):
        print("href", m.group(1))
    for m in re.finditer(r'"url":"(https?://[^"]+)"', chunk):
        print("url", m.group(1))
    for m in re.finditer(r'"link":\{[^}]+\}', chunk):
        print("link obj", m.group(0)[:300])

# page json name
m = re.search(
    r'"pageUriSEO":"about-1-2-1-1-2-1"[^}]*"pageJsonFileName":"([^"]+)"',
    page,
)
page_json = m.group(1) if m else None
print("page_json", page_json)

# thunderbolt
for link in re.findall(
    r"https://siteassets\.parastorage\.com/pages/pages/thunderbolt[^\"'\\]+",
    page,
):
    link = link.replace("\\/", "/")
    if "module=thunderbolt-features" in link and page_json and page_json in link:
        tb = urllib.request.urlopen(link, timeout=60).read().decode("utf-8", errors="ignore")
        for term in ["Read the Publication", "publication", "doi.org", "arxiv", "http"]:
            if term.lower() in tb.lower():
                pass
        for m in re.finditer(r'"url":"(https?://[^"]+)"', tb):
            u = m.group(1)
            if "wix" not in u and "parastorage" not in u:
                print("tb url", u)
        for m in re.finditer(r'"href":"(https?://[^"]+)"', tb):
            print("tb href", m.group(1))
        for m in re.finditer(r'Read the Publication[\s\S]{0,800}', tb):
            print("btn ctx", m.group(0)[:600])
        break
