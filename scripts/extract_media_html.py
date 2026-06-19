import re
import os

c = open(os.path.join(os.environ["TEMP"], "woodowel.html"), encoding="utf-8", errors="ignore").read()

# rendered HTML section
idx = c.find('id="comp-lyetmaz6"')
chunk = c[idx : idx + 25000]

for comp in ["lygha6r9", "lygh2qxw", "lyghcd84", "lyghsl5w", "lyghokp8"]:
    i = chunk.find(comp)
    print(f"\n=== {comp} ===")
    print(chunk[max(0, i - 200) : i + 1500][:1200])

# all src in media section
print("\n=== src urls in media section ===")
for u in re.findall(r'src="(https://static\.wixstatic\.com/[^"]+)"', chunk):
    print(u[:180])

# video mp4 anywhere
print("\n=== mp4 ===")
for u in sorted(set(re.findall(r"https://video\.wixstatic\.com/[^\"\\]+", c))):
    print(u)

for u in sorted(set(re.findall(r"007d85_35da901319324358b7b8500b93b87883[^\"\\]{0,200}", c))):
    print("35da:", u[:200])
