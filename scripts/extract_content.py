import re
import html
import os
import json

TMP = os.environ.get("TEMP", "/tmp")

PAGES = [
    ("index", "codesign.html"),
    ("about", "codesign-about.html"),
    ("about-1", "codesign-about-1.html"),
    ("about-1-1", "codesign-about-1-1.html"),
    ("about-1-2", "codesign-about-1-2.html"),
    ("about-1-2-1", "codesign-about-1-2-1.html"),
    ("about-1-2-1-1", "codesign-about-1-2-1-1.html"),
    ("about-1-2-1-1-1", "codesign-about-1-2-1-1-1.html"),
    ("about-1-2-1-1-2", "codesign-about-1-2-1-1-2.html"),
    ("about-1-2-1-1-2-1", "codesign-about-1-2-1-1-2-1.html"),
    ("about-1-2-1-1-2-2", "codesign-about-1-2-1-1-2-2.html"),
    ("about-1-3", "codesign-about-1-3.html"),
    ("about-1-3-1", "codesign-about-1-3-1.html"),
    ("contact", "codesign-contact.html"),
]


def strip_html(content):
    content = re.sub(r"<script[^>]*>.*?</script>", " ", content, flags=re.DOTALL | re.I)
    content = re.sub(r"<style[^>]*>.*?</style>", " ", content, flags=re.DOTALL | re.I)
    return content


def extract_page(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        raw = f.read()

    title_m = re.search(r"<title>([^<]+)</title>", raw)
    title = html.unescape(title_m.group(1)) if title_m else ""

    images = []
    for m in re.finditer(r'src="(https://static\.wixstatic\.com/media/[^"]+)"', raw):
        url = html.unescape(m.group(1))
        # prefer full-size without tiny dimensions
        if "blur_" not in url and url not in images:
            images.append(url)

    # fallback: srcset or other image patterns
    for m in re.finditer(r'"(https://static\.wixstatic\.com/media/[^"]+~mv2\.[^/]+/v1/[^"]+)"', raw):
        url = html.unescape(m.group(1))
        if url not in images:
            images.append(url)

    content = strip_html(raw)
    # wix rich text paragraphs
    paragraphs = []
    for m in re.finditer(r'wixui-rich-text__text[^>]*>([^<]+(?:<[^/][^>]*>[^<]*)*)', content):
        text = re.sub(r"<[^>]+>", " ", m.group(1))
        text = html.unescape(re.sub(r"\s+", " ", text)).strip()
        if len(text) > 2:
            paragraphs.append(text)

    if not paragraphs:
        for m in re.finditer(r">([^<>]{8,})<", content):
            text = html.unescape(re.sub(r"\s+", " ", m.group(1))).strip()
            if text and "wix" not in text.lower() and "function" not in text:
                paragraphs.append(text)

    seen = set()
    unique_paragraphs = []
    for p in paragraphs:
        if p not in seen:
            seen.add(p)
            unique_paragraphs.append(p)

    links = re.findall(r'href="(https://[^"]+)"', raw)

    return {
        "title": title,
        "paragraphs": unique_paragraphs[:60],
        "images": images[:10],
        "links": list(dict.fromkeys(links))[:20],
    }


def map_projects(home_html):
    blocks = re.findall(
        r"(\{0[0-9]\}[\s\S]{0,1200}?href=\"(https://www\.codesignexplore\.com/about[^\"]*)\")",
        home_html,
    )
    projects = []
    for block, url in blocks:
        text = re.sub(r"<[^>]+>", " ", block)
        text = html.unescape(re.sub(r"\s+", " ", text)).strip()
        slug = url.split("/")[-1]
        projects.append({"raw": text[:400], "url": url, "slug": slug})
    return projects


def main():
    home_path = os.path.join(TMP, "codesign.html")
    with open(home_path, encoding="utf-8", errors="ignore") as f:
        home_html = f.read()

    data = {"projects": map_projects(home_html), "pages": {}}

    for slug, filename in PAGES:
        path = os.path.join(TMP, filename)
        if os.path.exists(path):
            data["pages"][slug] = extract_page(path)

    out = os.path.join(os.path.dirname(__file__), "site_content.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
