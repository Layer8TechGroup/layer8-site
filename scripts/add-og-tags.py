#!/usr/bin/env python3
"""Add the full Open Graph / Twitter card block (advisory/index.html form) to
every page in sitemap.xml that lacks it. Uses each page's own title,
description, and canonical URL, with the shared og-image.jpg asset.

Reproducible: run from the repo root. Idempotent: pages already carrying the
block are skipped.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://layer8techgroup.com"
IMAGE = f"{SITE}/assets/images/og-image.jpg"

# Pages in sitemap.xml that currently lack the OG block (audit result).
TARGETS = [
    "advisory/compliance",
    "advisory/cipu",
    "advisory/assessment",
    "advisory/cloud",
    "advisory/ai-strategy",
    "advisory/fractional-cio",
    "advisory/identity",
    "advisory/ai-spend",
    "ai-services",
    "ai-services/automation",
    "ai-services/ocaas",
    "ai-services/ai-implementation",
    "infrastructure",
    "infrastructure/cabling",
    "infrastructure/av",
    "infrastructure/cctv",
    "infrastructure/wifi",
    "infrastructure/fiber",
    "infrastructure/access-control",
]


def build_block(title: str, desc: str, url: str) -> str:
    return (
        '  <meta property="og:type" content="website">\n'
        '  <meta property="og:site_name" content="Layer8 Tech Group">\n'
        f'  <meta property="og:title" content="{title}">\n'
        f'  <meta property="og:description" content="{desc}">\n'
        f'  <meta property="og:url" content="{url}">\n'
        f'  <meta property="og:image" content="{IMAGE}">\n'
        '  <meta property="og:image:width" content="1200">\n'
        '  <meta property="og:image:height" content="630">\n'
        '  <meta name="twitter:card" content="summary_large_image">\n'
        f'  <meta name="twitter:title" content="{title}">\n'
        f'  <meta name="twitter:description" content="{desc}">\n'
        f'  <meta name="twitter:image" content="{IMAGE}">\n'
    )


def main() -> None:
    changed = []
    for rel in TARGETS:
        path = ROOT / rel / "index.html"
        if not path.exists():
            print(f"SKIP (no file): {rel}")
            continue
        html = path.read_text(encoding="utf-8")
        if 'property="og:image"' in html:
            print(f"SKIP (already has og:image): {rel}")
            continue

        title = re.search(r"<title>(.*?)</title>", html, re.S)
        desc = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
        canon = re.search(r'<link rel="canonical" href="(.*?)"\s*/?>', html, re.S)
        if not title:
            print(f"ERROR (no title): {rel}")
            sys.exit(1)
        title = title.group(1).strip()
        desc = desc.group(1).strip() if desc else ""
        url = canon.group(1).strip() if canon else f"{SITE}/{rel}/"

        block = build_block(title, desc, url)

        # Insert after the full canonical tag (including its closing >) if
        # present, else after the description meta tag.
        if canon:
            anchor = canon.group(0)
        else:
            anchor = f'<meta name="description" content="{desc}">'
        if anchor not in html:
            print(f"ERROR (anchor not found): {rel}")
            sys.exit(1)
        html = html.replace(anchor, anchor + "\n" + block, 1)
        path.write_text(html, encoding="utf-8")
        changed.append(rel)
        print(f"UPDATED: {rel}")

    print(f"\n{len(changed)} page(s) updated.")


if __name__ == "__main__":
    main()
