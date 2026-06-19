import re
import os
import json
import urllib.request

c = open(os.path.join(os.environ["TEMP"], "woodowel.html"), encoding="utf-8", errors="ignore").read()
links = re.findall(r'https://siteassets\.parastorage\.com/pages/pages/thunderbolt[^"\']+', c)
for link in links:
    if "wiv9z" in link or True:
        print("Fetching...", link[:120], "...")
        try:
            with urllib.request.urlopen(link.replace("\\/", "/"), timeout=30) as r:
                data = r.read().decode("utf-8", errors="ignore")
            if "lygha6r9" in data or "video" in data.lower():
                open(os.path.join(os.environ["TEMP"], "thunderbolt.json"), "w", encoding="utf-8").write(data)
                print("saved, len", len(data))
                for term in ["lygha6r9", "videoUrl", "mp4", "007d85_35da", "qualities"]:
                    if term in data:
                        idx = data.find(term)
                        print(term, data[max(0, idx - 150) : idx + 500][:600])
                break
        except Exception as e:
            print("err", e)
