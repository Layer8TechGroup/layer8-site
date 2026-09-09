# layer8-site

Marketing site for **[layer8techgroup.com](https://layer8techgroup.com)** —
Layer8 Tech Group, a fractional technology leadership and AI advisory firm
(Marietta, Georgia).

Self-contained static HTML — no framework, no build step. Deploys to
layer8techgroup.com via **Cloudflare Pages** (GitHub integration — auto-builds
on push to `main`; serves at both apex and `www`).

## Structure

| Path | Page |
|------|------|
| `index.html` | Homepage — services-led (Advisory · Infrastructure · Automation) |
| `advisory/` | Technology Advisory (fractional CIO/CTO, infrastructure, compliance) |
| `about/` | About Layer8 + AI governance |
| `ai-services/` | **Hub** — orients between the AI service lines, does not sell any one of them |
| `ai-services/ocaas/` | OcaaS — Oversight as a Service (ongoing AI governance) |
| `ai-services/automation/` | Automation — inbound contact, capture, routing, follow-up |
| `404.html` | Not-found page (see "Soft-404" below) |
| `transaction-intelligence/` | Product pages — Exit Readiness, Due Diligence, Franchise, Deal Room *(kept for SEO; the seller-facing products now live on [sellerdiligence.com](https://sellerdiligence.com))* |
| `assets/css/main.css` | Shared design system (navy/teal/gold tokens) |
| `assets/js/main.js` | Nav, dropdown, mobile menu, scroll reveal |
| `_redirects` | 301s for legacy short URLs → canonical two-level paths |
| `docs/screenshots/` | Reference screenshots (below) |

## Nav is hard-coded — do not hand-copy a fourth variant

**The `/ai-services/` hub and `/ai-services/automation/` are linked from
`index.html` and from the hub only. This is deliberate. Do not "fix" it by
hand-editing the nav on the other pages.**

There is no build step and no partial injector, so the `<nav>` block is
hard-coded in full on every page. It has already drifted into three
incompatible variants:

1. `index.html` — a "Services" dropdown plus external product links; no
   Transaction Intelligence entries at all.
2. Eight pages (`about/`, `advisory/`, both `ai-services/*`, four of the five
   Transaction Intelligence pages) — a "Products" dropdown listing TI plus the
   external products. **Omits Deal Room.**
3. `transaction-intelligence/deal-room/` — includes Deal Room, drops the
   external product links.

The visible symptom: **Deal Room is reachable from the nav of exactly one page,
its own.** That is what nav drift costs, and it shipped because nothing in this
repo can block a merge or a deploy (no GitHub Actions, no Cloudflare build
command, no branch protection).

Hand-copying the new AI Services links into all eleven pages would create a
fourth variant and a fourth thing to keep in sync by hand. The real fix is to
consolidate the nav behind one injected partial — ported from
`sellerdiligence-site` (`_partials/`, `tools/sync-partials.py`) — and that is
filed as a follow-up issue, not done here. Until it lands, the limited linking
is the correct state, not an oversight.

`404.html` follows the same rule and deliberately carries brand chrome only,
with no `.nav-links` block, for the same reason.

## Soft-404

Cloudflare Pages serves the root `index.html` with **HTTP 200** for any
unmatched path when a project has no `404.html`. `_redirects` contains only
301s — there is no catch-all and no `200` rewrite — so the cause was simply the
missing file. Every mistyped or dead URL was returning a 200 with the homepage
body, which search engines index as duplicate content.

Adding `404.html` at the repo root fixes it. Because `destination_dir` is empty
and the repo root is the deployed artifact, the file needs no build wiring.
When verifying, **curl a nonsense path with a cache-busting query string first**
— a plain path may still be served from Cloudflare's edge cache from before the
fix, and will lie to you.

## Screenshots

### Homepage — desktop

<img src="docs/screenshots/home-desktop.png" alt="layer8techgroup.com homepage — desktop" width="800">

### Homepage — mobile

<img src="docs/screenshots/home-mobile.png" alt="layer8techgroup.com homepage — mobile" width="280">

### Deal Room product page

Desktop and mobile captures live at
[`docs/screenshots/deal-room-desktop.png`](docs/screenshots/deal-room-desktop.png)
and
[`docs/screenshots/deal-room-mobile.png`](docs/screenshots/deal-room-mobile.png).
