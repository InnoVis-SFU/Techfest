import re
import urllib.request

page = urllib.request.urlopen("https://www.codesignexplore.com/about", timeout=60).read().decode("utf-8", errors="ignore")
page_json = re.search(
    r'"pageUriSEO":"about"[^}]*"pageJsonFileName":"([^"]+)"',
    page,
).group(1)

for link in re.findall(
    r"https://siteassets\.parastorage\.com/pages/pages/thunderbolt[^\"'\\]+",
    page,
):
    link = link.replace("\\/", "/")
    if "module=thunderbolt-features" in link and page_json in link:
        tb = urllib.request.urlopen(link, timeout=60).read().decode("utf-8", errors="ignore")
        idx = 0
        while True:
            idx = tb.find('"fullNameCompType":"wixui.ImageX"', idx)
            if idx == -1:
                break
            start = tb.rfind('"comp-', idx - 80, idx)
            chunk = tb[start : start + 2000]
            uris = re.findall(r'"uri":"([^"]+~mv2\.[^"]+)"', chunk)
            wh = re.findall(r'"width":(\d+),"height":(\d+)', chunk)
            if uris:
                print(uris[0], wh[0] if wh else "")
            idx += 1
        break
