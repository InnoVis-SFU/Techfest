import re
import urllib.request

page = urllib.request.urlopen("https://www.codesignexplore.com/about", timeout=60).read().decode("utf-8", errors="ignore")
page_json = re.search(r'"pageUriSEO":"about"[^}]*"pageJsonFileName":"([^"]+)"', page).group(1)
for link in re.findall(r"https://siteassets\.parastorage\.com/pages/pages/thunderbolt[^\"'\\]+", page):
    link = link.replace("\\/", "/")
    if "module=thunderbolt-features" in link and page_json in link:
        tb = urllib.request.urlopen(link, timeout=60).read().decode("utf-8", errors="ignore")
        idx = 0
        while True:
            idx = tb.find('"pageId":"dkz1k"', idx)
            if idx == -1:
                break
            chunk = tb[max(0, idx - 800) : idx + 400]
            if "ImageX" in chunk and "uri" in chunk:
                uri = re.search(r'"uri":"([^"]+)"', chunk)
                if uri:
                    print(uri.group(1))
            idx += 1
        break
