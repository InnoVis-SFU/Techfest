#!/usr/bin/env python3
"""Download assets and generate the static Tech Fest site."""

from __future__ import annotations

import html
import json
import re
import os
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "images"
CSS_DIR = ROOT / "assets" / "css"
JS_DIR = ROOT / "assets" / "js"
PROJECTS_DIR = ROOT / "projects"

# Wix media id -> local filename
IMAGE_MAP = {
    "007d85_149815deb35041f1b1a6a80a7b3537b3~mv2.png": "hero-bg.png",
    "007d85_10a87d857a314ac99865ded900bbc630~mv2.png": "funder-nfrf.png",
    "007d85_b07c3ef63e3e400f988198bca56fc12d~mv2.png": "funder-crc.png",
    "007d85_96c90a005b4c403f856d2f9e76be810b~mv2.png": "funder-nserc.png",
    "007d85_c05db668dc1b4f7fa2bb8dc9bee80133~mv2.png": "logo-minimal.png",
    "007d85_31122b9c45ea4c66a7aa96ef9b92d4f4~mv2.png": "logo-bw.png",
    "007d85_39fbb9be60fb498a972236f16cbc5d09~mv2.png": "creative-coast-logo.png",
    "007d85_2044938ec1a04275b10e4c2a57821621~mv2.png": "project-data-comics.png",
    "d838ea_afae918e7ed14cf498c8a3cb1363543a~mv2.png": "project-kiriphys.png",
    "d838ea_345d85ea2132416aba3dcf823fc4ef61~mv2.jpg": "project-self-monitoring.jpg",
    "d838ea_480c496041d540c5bf957a71763d50ad~mv2.jpg": "project-vismock.jpg",
    "d838ea_549fecfba9c94d6ea7fc06bcce8fdb4a~mv2.png": "project-everyday-creativity.png",
    "d838ea_ef46fe1bcaba4892b6f8de91d4eaf034~mv2.png": "project-arts-funding.png",
    "d838ea_8b2af24bb17d4e3f814f52adfe42ca6f~mv2.jpg": "project-visualizations.jpg",
    "d838ea_03f11e3ef6f24c7db7b58c58a74bb3e7~mv2.png": "project-collective-action.png",
    "007d85_ff4baf3d7eba4596ba2693a080112616~mv2.png": "project-woodowel.png",
    "d838ea_cdf290e4948740c1a603ca5b942d8d9a~mv2.png": "project-tangibooks.png",
    "d838ea_b9d5536b94dc470b92ba6dda5e95f76a~mv2.png": "project-womens-print-history.png",
}

MEDIA_JSON = Path(__file__).resolve().parent / "project_media.json"

SITE_IMAGES = {
    "007d85_c05db668dc1b4f7fa2bb8dc9bee80133~mv2.png",
    "007d85_39fbb9be60fb498a972236f16cbc5d09~mv2.png",
    "007d85_31122b9c45ea4c66a7aa96ef9b92d4f4~mv2.png",
}

# Wix-hosted university logos were cropped; use official sources instead.
OFFICIAL_LOGOS = {
    "sfu-logo.png": "https://www.sfu.ca/etc/designs/clf/clientlibs/clf4/default/img/SFU@2x.png",
    "uvic-logo.svg": "https://www.uvic.ca/assets/core-4-0/img/uvic-wordmark-colour.svg",
}

PROJECTS = [
    {
        "num": "01",
        "slug": "woodowel",
        "title": "WooDowel: Innovative Plywood Sensor",
        "card_image": "project-woodowel.png",
        "contact": "Yanghao Shi",
        "members": "Yonghao Shi, Chenzheng Li, Yuning Su, Xing-Dong Yang, Te-Yen Wu",
        "description": [
            "We will be demonstrating a smart plywood that acts as a vibration sensor to detect various user activities, such as writing, occurring in contact with the plywood. Woodworkers can use this plywood to create smart furniture or household items.",
        ],
        "publication": "Shi, Y., Li, C., Su, Y., Yang, X. D., & Wu, T. Y. (2024, May). WooDowel: Electrode Isolation for Electromagnetic Shielding in Triboelectric Plywood Sensors. In Proceedings of the CHI Conference on Human Factors in Computing Systems (pp. 1-17).",
        "gallery": ["project-woodowel.png"],
    },
    {
        "num": "02",
        "slug": "data-comics",
        "title": "Communicating Permafrost Concepts with Data Comics",
        "card_image": "project-data-comics.png",
        "contact": "Zezhong Wang",
        "members": "Zezhong Wang, Stephan Gruber, Michelle Levy, Sheelagh Carpendale",
        "description": [
            "While there is a gap between what the general public and policymakers understand about science and what is known by experts, this gap is particularly perilous regarding climate change. Climate change is increasingly recognized as a paramount threat to life on the planet.",
            "The most recent report from the Intergovernmental Panel on Climate Change highlights the extreme and worsening impacts of climate change, including rising sea levels, heatwaves, drought, flooding, regional food, and water shortages, storm damage, and more.",
            "Scientists are generating massive amounts of data about climate change and developing significant understandings of the causal factors, wide-ranging projected impacts, and necessary mitigation and adaptation strategies. To know how to respond and make changes both policymakers and the general public need to be better supported to develop actionable comprehension.",
            "To close this gap, we have assembled a team that includes experts in data visualization, narrative construction, data comics, and climate change. We will work collaboratively to develop climate change data comics that combine compelling narratives with comprehensible data visuals that are informed and verified by the appropriate scientists.",
        ],
        "publication": "Wang, Z., Gruber, S., Levy, M., Carpendale, S. (2023). Data Comics for Understanding Climate Change.",
        "gallery": ["project-data-comics.png"],
    },
    {
        "num": "03",
        "slug": "kiriphys",
        "title": "Exploring new data physicalization opportunities with Kiriphys",
        "card_image": "project-kiriphys.png",
        "contact": "Foroozan Daneshzand",
        "members": "Foroozan Daneshzand, Charles Perin, Sheelagh Carpendale",
        "description": [
            "We are exploring the unique capabilities of Kirigami—the Japanese art of paper cutting—to represent data physically. This technique takes advantage of the tactile qualities of paper-cutting to introduce new data variables and tangible interactions. Paper is an accessible medium, and the versatility of this technique supports different scales, interactions, and functions, making it an excellent method for physicalizing data.",
        ],
        "publication": 'F. Daneshzand, C. Perin and S. Carpendale, "KiriPhys: Exploring New Data Physicalization Opportunities," in IEEE Transactions on Visualization and Computer Graphics, vol. 29, no. 1, pp. 225-235, Jan. 2023, doi: 10.1109/TVCG.2022.3209365.',
        "gallery": ["project-kiriphys.png"],
    },
    {
        "num": "04",
        "slug": "self-monitoring-tool",
        "title": "Designing a semi-automated self-monitoring tool for supporting self-directed learning of computational skills",
        "card_image": "project-self-monitoring.jpg",
        "contact": "Rimika Chaudhury",
        "members": "Rimika Chaudhury, Parmit Chilana",
        "description": [
            "Informal learners are taking up educational content online in unprecedented numbers, but these learners often find it difficult to self-direct their pursuits which may be spread across different mediums and study sessions. Inspired by self-monitoring interventions from domains such as health and productivity, we investigate how informal learners can better self-reflect on their learning experiences.",
            "We carried out two elicitation studies with paper-based and interactive prototypes to explore a range of designs for capturing and presenting learning data manually, automatically, and semi-automatically. Our synthesis of learners' perspectives on self-monitoring reveals that automatically generated visual overviews of learning histories are initially promising for increasing awareness. But, users also prefer having controls to manipulate overviews through personally relevant filtering options for better reflecting on their past, plan for future sessions, and communicate with others for feedback.",
        ],
        "publication": "Chaudhury, R., & Chilana, P. K. (2024). Designing Visual and Interactive Self-Monitoring Interventions to Facilitate Learning: Insights from Informal Learners and Experts. IEEE Transactions on Visualization and Computer Graphics.",
        "gallery": ["project-self-monitoring.jpg"],
    },
    {
        "num": "05",
        "slug": "vismock",
        "title": "VISMOCK Technique to Create Interactive Data Physicalizations",
        "card_image": "project-vismock.jpg",
        "contact": "Bahare Bakhtiari",
        "members": "Bahare Bakhtiari, Charles Perin, Sowmya Samanth",
        "description": [
            "We introduce VISMOCK, a data physicalization approach that leverages a fabric manipulation technique called \"smocking\". VISMOCK supports the creation of interactive and dynamic data physicalizations by extending the smocking technique with programmable components such as thermochromic pigments and shape memory alloys.",
            "Using a research-through-design methodology, we develop an initial design space for VISMOCK that shows how data can be represented using visual and tactile variables, as well as the affordances of VISMOCK. We demonstrate the generative power of our design space through four exemplars, created using VISMOCK.",
        ],
        "publication": "Bahare Bakhtiari, Charles Perin, and Sowmya Somanath. 2024. VISMOCK: A Programmable Smocking Technique for Creating Interactive Data Physicalization. In Proceedings of the 2024 ACM Designing Interactive Systems Conference (DIS '24). https://doi.org/10.1145/3643834.3660749",
        "gallery": ["project-vismock.jpg"],
    },
    {
        "num": "06",
        "slug": "tangibooks",
        "title": "TangiBooks Authoring Tool",
        "card_image": "project-tangibooks.png",
        "contact": "David Wong-Aitken",
        "members": "David Wong-Aitken, Parsa Rajabi, Sheelagh Carpendale, Parmit Chilana",
        "description": [
            "In recent years, researchers have explored innovative approaches to enhance the learning experience by incorporating tangible objects into learning. Notably, tangibles combined with electronics have gained popularity as effective tools for learning.",
            "Taking into consideration the design space of paper-and-electronics based manipulatives, we built TangiBook, a hardware platform and cloud-based app to investigate how instructors can create lessons through paper and electronics. With them, instructors don't need to learn how to deal with electronics or hardware, focusing exclusively on their lesson design, providing comfort and design freedom.",
        ],
        "publication": "Wong-Aitken, D., Rajabi, P., Carpendale, S., & Chilana, P. K. (2023, October). TangiBooks: Design and Creation of Paper-Based Tangibles with Embedded Electronics for Teaching Programming Concepts. In 2023 IEEE Symposium on Visual Languages and Human-Centric Computing (VL/HCC) (pp. 12-24). IEEE.",
        "gallery": ["project-tangibooks.png"],
    },
    {
        "num": "07",
        "slug": "everyday-creativity",
        "title": "Everyday Creativity: Technologies for Making, Learning, and Communication",
        "card_image": "project-everyday-creativity.png",
        "contact": "Sowmya Samanth",
        "members": "Sabrina Lakhdhir, Chehak Nayar, Fraser Anderson, Helene Fournier, Liisa Holsti, Irina Kondratova, Charles Perin, Jessi Stark, George Fitzmaurice, Lora Oehlberg, Ehud Sharlin, Sowmya Samanth",
        "description": [
            "Our research focuses on facilitating everyday forms of creativity. We do things like:",
            "Build new design tools – we design technologies that help people create personalized objects like custom blood glucose monitors.",
            "Create interactive mediums for communication – we explore how everyday items such as clothes, fabric, and woven artifacts can be used to communicate information.",
            "Make interactions accessible – we build technologies that can help learning STEM concepts more accessible.",
        ],
        "publication": "Sabrina Lakhdhir, Chehak Nayar, Fraser Anderson, Helene Fournier, Liisa Holsti, Irina Kondratova, Charles Perin, and Sowmya Somanath. 2024. GlucoMaker: Enabling Collaborative Customization of Glucose Monitors. In Proceedings of the CHI Conference on Human Factors in Computing Systems (CHI '24). https://doi.org/10.1145/3613904.3642435",
        "gallery": ["project-everyday-creativity.png"],
    },
    {
        "num": "08",
        "slug": "arts-funding",
        "title": "Who Gets What: Visualizing Canada's Arts Funding",
        "card_image": "project-arts-funding.png",
        "contact": "Wei Wei",
        "members": "Wei Wei, Sheelagh Carpendale, Charles Perin",
        "description": [
            "This ongoing project stems from a collaboration with Creative Coast (https://www.creativecoast.ca/).",
        ],
        "publication": None,
        "gallery": ["project-arts-funding.png"],
    },
    {
        "num": "09",
        "slug": "comprehensible-visualizations",
        "title": "Towards more comprehensible visualizations",
        "card_image": "project-visualizations.jpg",
        "contact": "Maryam Rezaie",
        "members": "Maryam Rezaie, Melanie Tory, Sheelagh Carpendale",
        "description": [
            "The visualization community recognizes the challenges people face in understanding complex visual data. Through an empirical study, my research has detailed the difficulties encountered in the visualization sensemaking process and the strategies visualization viewers employ to overcome these challenges.",
            "Our findings inform the design and integration of interactions, inspired by natural user behaviors, into self-explanatory visualizations that are accessible and beneficial to all.",
        ],
        "publication": 'M. Rezaie, M. Tory and S. Carpendale, "Struggles and Strategies in Understanding Information Visualizations," in IEEE Transactions on Visualization and Computer Graphics, vol. 30, no. 6, pp. 3035-3048, June 2024, doi: 10.1109/TVCG.2024.3388560.',
        "gallery": ["project-visualizations.jpg"],
    },
    {
        "num": "10",
        "slug": "collective-action",
        "title": "Supporting collective action with data",
        "card_image": "project-collective-action.png",
        "contact": "Nicholas Vincent",
        "members": "Nicholas Vincent",
        "description": [
            "Many kinds of creative activities have the potential to support AI systems because the artifacts of such activities can be used as training data. However, the current practices in the AI community sometimes use such data without consent and/or compensation.",
            "This data is very critical to the success of AI, so creators have potential leverage over companies and other bodies using AI. This project will aim to build a suite of tools to measure and communicate the value and potential of such data.",
        ],
        "publication": None,
        "publication_url": "https://scholar.archive.org/work/e3giylpikvbcrakiv57g7ojwbe/access/wayback/https://arch.library.northwestern.edu/downloads/vm40xs06k",
        "publication_link_text": "Read the Publication",
        "gallery": ["project-collective-action.png"],
    },
    {
        "num": "11",
        "slug": "womens-print-history",
        "title": "Supporting Exploration of Women's Print History Project Dataset",
        "card_image": "project-womens-print-history.png",
        "contact": "Parnian Taghipour",
        "members": "Parnian Taghipour, Maryam Rezaie, Michelle Levy, Thomas Shermer, Sheelagh Carpendale",
        "description": [
            "We designed, developed, and studied a visualization, WPHPVis, to support the exploration of the Women's Print History Project (WPHP) data. WPHP are collecting a bibliography that spans the years 1700 to 1836 recording information about books in which women have been involved through a number of roles including as authors, editors, translators, publishers, printers and booksellers.",
            "By working directly with WPHP experts to focus on their understanding, their research practices, and needs we co-designed WPHPVis using interactive construction of network links to support exploration of their data. We then studied the responses of both data experts and more general users.",
            "Through our qualitative study with both experts and non-experts, we learned about how the tool supported the WPHP experts' research practices as well as about how to improve overall interactive experience. We conclude by discussing the importance of representing missing data, the advantages of striking a balance between visualization structure and explorability, and the opportunities enabled by co-design with domain experts.",
        ],
        "publication": "Parnian Taghipour, Maryam Rezaie, Michelle Levy, Thomas Shermer, and Sheelagh Carpendale. 2024. Supporting Exploration of Women's Print History Project Data via Interactively Constructing Networks of Interest. In Proceedings of the 2024 International Conference on Advanced Visual Interfaces (AVI '24). https://doi.org/10.1145/3656650.3656697",
        "gallery": ["project-womens-print-history.png"],
    },
]


def local_to_wix() -> dict[str, str]:
    return {filename: media_id for media_id, filename in IMAGE_MAP.items()}


def project_exclude_ids(project: dict) -> set[str]:
    filename_to_wix = local_to_wix()
    exclude = set(SITE_IMAGES)
    for key in ("card_image", *project.get("gallery", [])):
        wix_id = filename_to_wix.get(key)
        if wix_id:
            exclude.add(wix_id)
    return exclude


def media_local_name(slug: str, index: int, wix_id: str) -> str:
    ext = wix_id.rsplit(".", 1)[-1]
    return f"{slug}-media-{index:02d}.{ext}"


def apply_project_media() -> None:
    if not MEDIA_JSON.exists():
        print(f"No {MEDIA_JSON.name}; run scripts/fetch_project_media.py first.")
        return

    raw = json.loads(MEDIA_JSON.read_text(encoding="utf-8"))
    for project in PROJECTS:
        slug = project["slug"]
        entry = raw.get(slug, {})
        exclude = project_exclude_ids(project)
        wix_ids = [mid for mid in entry.get("images", []) if mid not in exclude]
        local_images: list[str] = []

        for index, wix_id in enumerate(wix_ids, start=1):
            filename = media_local_name(slug, index, wix_id)
            IMAGE_MAP[wix_id] = filename
            local_images.append(filename)

        video = entry.get("video")
        if not local_images and not video:
            local_images = list(project.get("gallery", []))

        if local_images or video:
            project["media"] = {"video": video, "images": local_images}


def wix_url(media_id: str, width: int = 1200) -> str:
    ext = media_id.rsplit(".", 1)[-1]
    return (
        f"https://static.wixstatic.com/media/{media_id}/v1/fill/w_{width},h_{width},al_c,q_85/"
        f"{media_id.rsplit('~', 1)[0]}.{ext}"
    )


def wix_original_url(media_id: str) -> str:
    return f"https://static.wixstatic.com/media/{media_id}"


def download_official_logos() -> None:
    for filename, url in OFFICIAL_LOGOS.items():
        dest = ASSETS / filename
        print(f"Downloading {filename} (official)...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                dest.write_bytes(response.read())
        except Exception as exc:
            print(f"  Failed {filename}: {exc}")


def download_images() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    download_official_logos()
    use_original = {
        name
        for name in IMAGE_MAP.values()
        if name.startswith("funder-")
        or name.startswith("project-")
        or "-media-" in name
    }
    for media_id, filename in IMAGE_MAP.items():
        dest = ASSETS / filename
        if dest.exists() and filename not in use_original:
            continue
        url = wix_original_url(media_id) if filename in use_original else wix_url(media_id)
        print(f"Downloading {filename}...")
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as exc:
            print(f"  Failed {filename}: {exc}")


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def nav(current: str, prefix: str = "") -> str:
    items = [
        ("index.html", "Home", current == "home"),
        ("organizers.html", "Tech Fest Organizers", current == "organizers"),
        ("contact.html", "Contact", current == "contact"),
    ]
    links = []
    for href, label, active in items:
        cls = ' class="active"' if active else ""
        links.append(f'<li><a href="{prefix}{href}"{cls}>{esc(label)}</a></li>')
    return "\n".join(links)


def partners_strip(base: str = "") -> str:
    return f"""
  <footer class="site-partners" aria-label="Partner institutions">
    <img src="{base}assets/images/partners-strip.png" alt="Creative Coast, Simon Fraser University, and University of Victoria" class="partners-strip">
  </footer>"""


def page_shell(
    title: str,
    current: str,
    body: str,
    prefix: str = "",
    depth: int = 0,
    body_class: str = "",
) -> str:
    base = "../" * depth if depth else ""
    body_attr = f' class="{body_class}"' if body_class else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)} | Tech Fest</title>
  <meta name="description" content="Tech Fest – exploring new technology from Simon Fraser University and University of Victoria.">
  <link rel="icon" href="{base}assets/images/logo-minimal.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Questrial&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{base}assets/css/styles.css">
</head>
<body{body_attr}>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="{base}index.html">
        <img src="{base}assets/images/logo-techfest.png" alt="Tech Fest logo" width="67" height="48">
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
      <nav id="site-nav" class="site-nav" aria-label="Main">
        <ul>
          {nav(current, prefix if depth else "")}
        </ul>
      </nav>
    </div>
  </header>
  <main id="main">
    {body}
  </main>
  {partners_strip(base)}
  <script src="{base}assets/js/main.js"></script>
</body>
</html>
"""


def build_index() -> str:
    cards = []
    for p in PROJECTS:
        cards.append(
            f"""
        <article class="project-card">
          <span class="project-num">{esc(p['num'])}</span>
          <h3>{esc(p['title'])}</h3>
          <div class="project-card-image">
            <img src="assets/images/{esc(p['card_image'])}" alt="" loading="lazy">
          </div>
          <p class="project-contact"><strong>Explore this project with:</strong> {esc(p['contact'])}</p>
          <p class="project-members"><strong>Project members:</strong> {esc(p['members'])}</p>
          <a class="btn btn-outline" href="projects/{esc(p['slug'])}.html">Read More</a>
        </article>"""
        )

    body = f"""
    <section class="hero" aria-label="Tech Fest introduction">
      <div class="hero-panel">
        <div class="hero-main">
          <img class="hero-decor" src="assets/images/hero-bg.png" alt="" aria-hidden="true">
          <div class="hero-layout">
            <div class="hero-brand">
              <div class="hero-circle">
                <p class="hero-circle-label">Exhibition &amp; Discussion</p>
                <p class="hero-circle-title">tech fest</p>
              </div>
            </div>
            <div class="hero-event">
              <p class="hero-memory">In the memory of a successful tech festival held on July 31, 2024.</p>
              <p>Morning session: 10:00 AM – 12:00 PM (Invitation only)</p>
              <p>Afternoon Session: 2:00 – 4:00 PM (Everyone is welcome)</p>
              <h2>Location:</h2>
              <p>Room 660. Engineering &amp; Computer Science Building, University of Victoria</p>
            </div>
          </div>
        </div>
        <div class="hero-funders">
          <p class="hero-funders-text">Thanks to our funders for making this possible:</p>
          <div class="hero-funder-logos">
            <img src="assets/images/funder-nfrf.png" alt="New Frontiers in Research Fund">
            <img src="assets/images/funder-nserc.png" alt="NSERC CRSNG">
            <img src="assets/images/funder-crc.png" alt="Canada Research Chairs">
          </div>
        </div>
      </div>
    </section>

    <section class="section projects-section" id="projects">
      <div class="projects-panel">
        <div class="projects-intro">
          <div class="projects-intro-card">
            <p class="projects-lead">Explore some of the new technology being developed at <strong>Simon Fraser University</strong> and <strong>University of Victoria</strong>.</p>
            <div class="projects-topics">
              <p class="topics-label">Examples of latest research in:</p>
              <ul class="topic-tags">
                <li>Data visualization</li>
                <li>Data activism</li>
                <li>Smart materials</li>
                <li>Human-computer interaction</li>
              </ul>
            </div>
          </div>
        </div>
        <header class="projects-header">
          <h2 class="projects-title">Projects</h2>
        </header>
        <div class="project-grid">
          {''.join(cards)}
        </div>
      </div>
    </section>
    """
    return page_shell("Home", "home", body, body_class="page-home")


def build_organizers() -> str:
    body = """
    <section class="section">
      <div class="container narrow">
        <h1>Tech Fest Organizers</h1>
      </div>
      <div class="container organizers-grid">
        <div class="org-block">
          <div class="org-logo-frame">
            <img src="assets/images/sfu-logo.png" alt="Simon Fraser University" class="org-logo">
          </div>
          <h2>Simon Fraser University</h2>
          <ul class="org-list">
            <li><strong>Sheelagh Carpendale</strong></li>
            <li><strong>Narges Ashtari</strong><br><span class="role">Tech Fest coordinator &amp; website designer</span></li>
            <li><strong>Nastaran Sedehi</strong><br><span class="role">Tech Fest coordinator, graphics &amp; website designer</span></li>
          </ul>
        </div>
        <div class="org-block">
          <div class="org-logo-frame">
            <img src="assets/images/uvic-logo.svg" alt="University of Victoria" class="org-logo">
          </div>
          <h2>University of Victoria</h2>
          <ul class="org-list">
            <li><strong>Charles Perin</strong></li>
            <li><strong>Wei Wei</strong><br><span class="role">Tech Fest coordinator</span></li>
            <li><strong>Sarian Kashanji</strong><br><span class="role">Tech Fest coordinator</span></li>
          </ul>
        </div>
      </div>
    </section>
    """
    return page_shell("Tech Fest Organizers", "organizers", body, body_class="page-organizers")


def build_contact() -> str:
    body = """
    <section class="section contact-page">
      <div class="contact-page-inner">
        <h1>Contact</h1>
        <p class="lead">Let us know what you think!</p>
        <form class="contact-form" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
          <div class="form-row">
            <label for="first-name">First name</label>
            <input id="first-name" name="first_name" type="text" autocomplete="given-name" required>
          </div>
          <div class="form-row">
            <label for="last-name">Last name</label>
            <input id="last-name" name="last_name" type="text" autocomplete="family-name" required>
          </div>
          <div class="form-row">
            <label for="email">Email</label>
            <input id="email" name="email" type="email" autocomplete="email" required>
          </div>
          <div class="form-row">
            <label for="message">Message</label>
            <textarea id="message" name="message" rows="6" required></textarea>
          </div>
          <button class="btn btn-primary" type="submit">Submit</button>
        </form>
        <p class="contact-alt">Or email the organizers via the <a href="organizers.html">Organizers page</a>.</p>
      </div>
    </section>
    """
    return page_shell("Contact", "contact", body)


def build_project(p: dict) -> str:
    desc_html = "".join(f"<p>{esc(d)}</p>" for d in p["description"])
    pub_html = ""
    if p.get("publication") or p.get("publication_url"):
        pub_body = ""
        if p.get("publication"):
            pub_body += f'<p class="publication">{esc(p["publication"])}</p>'
        if p.get("publication_url"):
            link_text = p.get("publication_link_text", "Read the publication")
            pub_body += (
                f'<p class="publication-link"><a class="btn btn-outline" '
                f'href="{esc(p["publication_url"])}" target="_blank" '
                f'rel="noopener noreferrer">{esc(link_text)}</a></p>'
            )
        pub_html = f"""
        <div class="project-block">
          <h2>Most Recent Publication</h2>
          {pub_body}
        </div>"""
    media_html = ""
    media = p.get("media")
    if media:
        items: list[str] = []
        if media.get("video"):
            items.append(
                f"""
            <figure class="project-media-item project-media-video">
              <iframe src="{esc(media['video'])}" title="Project video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen loading="lazy"></iframe>
            </figure>"""
            )
        for img in media.get("images", []):
            items.append(
                f"""
            <figure class="project-media-item">
              <img src="../assets/images/{esc(img)}" alt="" loading="lazy">
            </figure>"""
            )
        if items:
            media_html = f"""
        <div class="project-block project-media">
          <h2>Media</h2>
          <div class="project-media-stack">{''.join(items)}
          </div>
        </div>"""
    gallery_html = "".join(
        f'<img src="../assets/images/{esc(img)}" alt="" loading="lazy">' for img in p.get("gallery", [])
    )
    body = f"""
    <section class="section page-header project-header">
      <div class="container narrow">
        <span class="project-num">{esc(p['num'])}</span>
        <h1>{esc(p['title'])}</h1>
        <p><strong>Explore this project with:</strong> {esc(p['contact'])}</p>
        <p><strong>Project members:</strong> {esc(p['members'])}</p>
      </div>
    </section>
    <section class="section">
      <div class="container narrow project-body">
        <div class="project-gallery">{gallery_html}</div>
        <div class="project-block">
          <h2>Project Description</h2>
          {desc_html}
        </div>
        {pub_html}
        {media_html}
        <p><a class="btn btn-outline" href="../index.html#projects">← Back to all projects</a></p>
      </div>
    </section>
    """
    return page_shell(p["title"], "home", body, prefix="../", depth=1)


def main() -> None:
    apply_project_media()
    download_images()
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

    (ROOT / "index.html").write_text(build_index(), encoding="utf-8")
    (ROOT / "organizers.html").write_text(build_organizers(), encoding="utf-8")
    (ROOT / "contact.html").write_text(build_contact(), encoding="utf-8")

    for p in PROJECTS:
        path = PROJECTS_DIR / f"{p['slug']}.html"
        path.write_text(build_project(p), encoding="utf-8")

    print(f"Generated site in {ROOT}")


if __name__ == "__main__":
    main()
