#!/usr/bin/env python3
"""Fetch page JSON from Wix and extract media for each project page."""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://www.codesignexplore.com"
SITE_ASSETS = "https://siteassets.parastorage.com/pages/pages"

# slug -> wix path (verified from pagesMap + homepage order)
WIX_PATHS = {
    "woodowel": "about-1",
    "data-comics": "about-1-1",
    "kiriphys": "about-1-2",
    "self-monitoring-tool": "about-1-3",
    "vismock": "about-1-2-1",
    "tangibooks": "about-1-3-1",
    "everyday-creativity": "about-1-2-1-1",
    "arts-funding": "about-1-2-1-1-1",
    "comprehensible-visualizations": "about-1-2-1-1-2",
    "collective-action": "about-1-2-1-1-2-1",
    "womens-print-history": "about-1-2-1-1-2-2",
}

SITE_IMAGES = {
    "007d85_c05db668dc1b4f7fa2bb8dc9bee80133~mv2.png",
    "007d85_7782dfb2b6564e57bc7fdabebd256e50~mv2.jpg",
    "007d85_b4274974a593411db5103c2c46fe555f~mv2.png",
    "007d85_39fbb9be60fb498a972236f16cbc5d09~mv2.png",
    "007d85_31122b9c45ea4c66a7aa96ef9b92d4f4~mv2.png",
}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="ignore")


def youtube_embed(url: str) -> str | None:
    m = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)", url)
    return f"https://www.youtube.com/embed/{m.group(1)}" if m else None


def page_json_name(html: str, wix_path: str) -> str | None:
    m = re.search(
        rf'"pageUriSEO":"{re.escape(wix_path)}"[^}}]*"pageJsonFileName":"([^"]+)"',
        html,
    )
    return m.group(1) if m else None


def thunderbolt_url(html: str, page_json: str) -> str | None:
    for link in re.findall(
        r"https://siteassets\.parastorage\.com/pages/pages/thunderbolt[^\"'\\]+",
        html,
    ):
        link = link.replace("\\/", "/")
        if "module=thunderbolt-features" in link and f"pageId={urllib.parse.quote(page_json, safe='')}" in link:
            return link
        if "module=thunderbolt-features" in link and f"pageId={page_json}" in link:
            return link
    # build from template on page
    for link in re.findall(
        r"https://siteassets\.parastorage\.com/pages/pages/thunderbolt[^\"'\\]+",
        html,
    ):
        link = link.replace("\\/", "/")
        if "module=thunderbolt-features" in link:
            return re.sub(r"pageId=[^&]+", f"pageId={page_json}", link)
    return None


def extract_media_from_json(text: str, gallery_id: str | None) -> dict:
    video = None
    for m in re.finditer(
        r'"src":"(https://(?:www\.)?(?:youtube\.com/watch\?v=[^"]+|youtu\.be/[^"]+))"',
        text,
    ):
        video = youtube_embed(m.group(1))
        break

    images: list[str] = []
    seen: set[str] = set()
    idx = 0
    while True:
        idx = text.find('"fullNameCompType":"wixui.ImageX"', idx)
        if idx == -1:
            break
        start = text.rfind('"comp-', idx - 80, idx)
        chunk = text[start : start + 2000]
        for uri in re.findall(r'"uri":"([^"]+~mv2\.[^"]+)"', chunk):
            if uri in seen or uri in SITE_IMAGES:
                continue
            if gallery_id and uri == gallery_id:
                continue
            seen.add(uri)
            images.append(uri)
        idx += 1

    return {"video": video, "images": images}


def main() -> None:
    home = fetch(BASE)
    out: dict = {}

    for slug, wix_path in WIX_PATHS.items():
        print(f"{slug} ({wix_path})...")
        page_html = fetch(f"{BASE}/{wix_path}")
        page_json = page_json_name(home, wix_path) or page_json_name(page_html, wix_path)
        if not page_json:
            print("  no page json")
            out[slug] = {"video": None, "images": []}
            continue

        tb_url = thunderbolt_url(page_html, page_json)
        if not tb_url:
            print(f"  no thunderbolt url for {page_json}")
            out[slug] = {"video": None, "images": []}
            continue

        tb = fetch(tb_url)
        media = extract_media_from_json(tb, gallery_id=None)
        if not media["images"] and not media["video"]:
            # fallback: page HTML minus site images
            imgs = []
            for m in re.finditer(r"wixstatic\.com/media/([a-f0-9_]+~mv2\.[a-z]+)", page_html):
                mid = m.group(1)
                if mid not in SITE_IMAGES and mid not in imgs:
                    imgs.append(mid)
            media["images"] = imgs[1:] if len(imgs) > 1 else imgs  # drop first gallery
            media["source"] = "html-fallback"

        out[slug] = media
        print(
            f"  json={page_json}, video={'yes' if media['video'] else 'no'}, "
            f"images={len(media['images'])}"
        )
        for img in media["images"]:
            print(f"    {img}")

    dest = Path(__file__).resolve().parent / "project_media.json"
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {dest}")


if __name__ == "__main__":
    main()
