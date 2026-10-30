"""
Catalogue audit for https://automationexercise.com

Checks every product available at run time and writes a timestamped report.

For each product:
  - name and price agree across the API (productsList), the catalogue page (/products) and the product page
  - product page and main image respond with HTTP 200
  - product page has a <title>, an <h1> and alt text on the main image
It also flags content worth a human review (judgement, kept separate from the factual checks)
and lists every check that could not be completed.

Usage (from the repository root, Python 3.8+, no extra packages):
    python scripts/catalogue_audit.py

Output (catalogue/reports/):
    catalogue_<timestamp>.csv      one row per product, every check
    catalogue_<timestamp>.md       readable summary for content, SEO and development
    api_productsList_<timestamp>.json   raw API response used for the run
    latest.csv / latest.md         copies of the newest run

Requests are sent one at a time with a short pause; this is a read-only check, not a load test.
"""

import csv
import datetime
import html
import json
import re
import shutil
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://automationexercise.com"
TIMEOUT = 20
RETRIES = 2
PAUSE = 0.2
USER_AGENT = "Mozilla/5.0 (QA catalogue audit; read-only)"

OUT_DIR = Path(__file__).resolve().parent.parent / "catalogue" / "reports"

# Columns of the CSV, in order
FIELDS = [
    "checked_at", "product_id", "pdp_url", "attention",
    "api_name", "catalogue_name", "pdp_name", "name_match",
    "api_price", "catalogue_price", "pdp_price", "price_match",
    "api_brand", "pdp_brand", "brand_match",
    "pdp_http_status", "main_image_url", "main_image_http_status", "main_image_ok",
    "page_title", "has_page_title", "title_names_product",
    "h1_count", "has_h1", "product_heading_tag",
    "main_image_alt", "has_alt", "alt_names_product",
    "facts_failed", "content_review", "checks_not_completed",
]


# ---------- HTTP ----------

def fetch(url, data=None):
    """Return (status, content_type, body_text, error). status is None if the request failed after retries."""
    body = None if data is None else urllib.parse.urlencode(data).encode()
    last_error = ""
    for attempt in range(RETRIES + 1):
        try:
            req = urllib.request.Request(url, data=body, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                raw = r.read()
                ctype = r.headers.get("Content-Type", "")
                text = raw.decode("utf-8", "replace") if not ctype.startswith("image/") else ""
                return r.status, ctype, text, ""
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get("Content-Type", ""), "", ""
        except Exception as e:  # timeout, DNS, connection reset...
            last_error = f"{type(e).__name__}: {e}"
            time.sleep(1 + attempt)
    return None, "", "", last_error


# ---------- Parsing helpers ----------

def clean(text):
    """Strip tags, decode entities, collapse whitespace."""
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def price_value(text):
    m = re.search(r"Rs\.?\s*([\d,]+)", text or "")
    return int(m.group(1).replace(",", "")) if m else None


def parse_catalogue(page):
    """Product cards on /products -> {id: {name, price}}"""
    cards = {}
    for block in re.findall(r'<div class="productinfo text-center">(.*?)</div>', page, re.S):
        pid = re.search(r'data-product-id="(\d+)"', block)
        if not pid:
            continue
        cards[int(pid.group(1))] = {
            "name": clean(re.search(r"<p>(.*?)</p>", block, re.S).group(1)) if "<p>" in block else "",
            "price": clean(re.search(r"<h2>(.*?)</h2>", block, re.S).group(1)) if "<h2>" in block else "",
        }
    return cards


def parse_product_page(page):
    title = re.search(r"<title>(.*?)</title>", page, re.S)
    info = re.search(r'<div class="product-information">(.*?)</div>', page, re.S)
    info = info.group(1) if info else ""
    heading = re.search(r"<(h[1-6])>(.*?)</\1>", info, re.S)
    price = re.search(r"<span>\s*(Rs\.[^<]*)</span>", info)
    brand = re.search(r"<b>Brand:</b>([^<]*)</p>", info)
    image = re.search(r'<div class="view-product">\s*<img([^>]*)>', page, re.S)
    img_attrs = image.group(1) if image else ""
    src = re.search(r'src="([^"]*)"', img_attrs)
    alt = re.search(r'alt="([^"]*)"', img_attrs)
    return {
        "title": clean(title.group(1)) if title else "",
        "h1_count": len(re.findall(r"<h1[\s>]", page, re.I)),
        "heading_tag": heading.group(1) if heading else "",
        "name": clean(heading.group(2)) if heading else "",
        "name_raw": html.unescape(heading.group(2)) if heading else "",
        "price": clean(price.group(1)) if price else "",
        "brand": clean(brand.group(1)) if brand else "",
        "image_src": src.group(1) if src else "",
        "image_alt": html.unescape(alt.group(1)) if alt else None,  # None = attribute missing
    }


def yn(value):
    return "Y" if value else "N"


# ---------- Content review (judgement, not pass/fail) ----------

def content_review(api_name, pdp, generic_alts):
    notes = []
    if api_name and api_name.isupper():
        notes.append("Name is in capitals - check house style")
    if pdp["name_raw"] and re.search(r"\S\s{2,}\S", pdp["name_raw"].strip()):
        notes.append("Product page heading has extra spaces")
    if api_name and len(api_name) > 50:
        notes.append("Long name (>50 characters) - may truncate on cards")
    if api_name and re.search(r"\s-\S|\S-\s", api_name):  # space on one side of the hyphen only
        notes.append("Inconsistent spacing around '-' (most names use ' - ')")
    if api_name and re.search(r"[–—]", api_name):
        notes.append("Uses a long dash (–) where other names use '-'")
    if pdp["image_alt"] and pdp["image_alt"] in generic_alts:
        notes.append(f'Alt text is generic ("{pdp["image_alt"]}") - not useful to screen-reader users')
    if pdp["title"] and api_name and api_name.lower() not in pdp["title"].lower():
        notes.append("Page title does not name the product - weak for SEO and browser tabs")
    return "; ".join(notes)


# ---------- Main ----------

def main():
    started = time.time()
    now = datetime.datetime.now().astimezone()
    offset = now.strftime("%z")
    checked_at = now.strftime("%Y-%m-%d %H:%M") + f" (UTC{offset[:3]}:{offset[3:]})"
    stamp = now.strftime("%Y%m%d_%H%M")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Catalogue audit - {checked_at}")

    # 1. API
    status, _, api_text, err = fetch(f"{BASE}/api/productsList")
    try:
        api_products = {p["id"]: p for p in json.loads(api_text)["products"]}
    except Exception:
        print(f"STOP: API productsList unavailable (HTTP {status} {err}). No report written.")
        sys.exit(2)
    (OUT_DIR / f"api_productsList_{stamp}.json").write_text(api_text, encoding="utf-8")
    print(f"  API productsList: HTTP {status}, {len(api_products)} products")

    # 2. Catalogue page
    cat_status, _, cat_page, cat_err = fetch(f"{BASE}/products")
    catalogue = parse_catalogue(cat_page) if cat_status == 200 else {}
    print(f"  Catalogue /products: HTTP {cat_status or 'failed'}, {len(catalogue)} product cards")

    all_ids = sorted(set(api_products) | set(catalogue))
    rows = []

    # 3. Each product page + main image
    for pid in all_ids:
        time.sleep(PAUSE)
        api = api_products.get(pid, {})
        card = catalogue.get(pid, {})
        url = f"{BASE}/product_details/{pid}"
        not_done = []

        pdp_status, _, pdp_page, pdp_err = fetch(url)
        if pdp_status is None:
            not_done.append(f"Product page request failed ({pdp_err})")
        pdp = parse_product_page(pdp_page) if pdp_status == 200 else parse_product_page("")
        if pdp_status == 200 and not pdp["name"]:
            not_done.append("Product page returned 200 but no product information")

        img_url = urllib.parse.urljoin(BASE, pdp["image_src"]) if pdp["image_src"] else ""
        img_status, img_type = None, ""
        if img_url:
            time.sleep(PAUSE)
            img_status, img_type, _, img_err = fetch(img_url)
            if img_status is None:
                not_done.append(f"Image request failed ({img_err})")
        elif pdp_status == 200:
            not_done.append("Main image not found in page")

        if not api:
            not_done.append("Product missing from API")
        if not card:
            not_done.append("Product missing from catalogue page" if cat_status == 200 else "Catalogue page unavailable")

        # Name and price: compare only the sources that were available
        names = [n for n in (api.get("name"), card.get("name"), pdp["name"]) if n]
        prices = [p for p in (price_value(api.get("price")), price_value(card.get("price")), price_value(pdp["price"])) if p is not None]
        name_match = yn(len(names) == 3 and len({clean(n) for n in names}) == 1) if len(names) == 3 else "not checked"
        price_match = yn(len(prices) == 3 and len(set(prices)) == 1) if len(prices) == 3 else "not checked"

        product_name = clean(api.get("name") or pdp["name"])
        has_alt = bool(pdp["image_alt"] and pdp["image_alt"].strip())
        image_ok = img_status == 200 and img_type.startswith("image/")

        row = {
            "checked_at": checked_at, "product_id": pid, "pdp_url": url,
            "api_name": api.get("name", ""), "catalogue_name": card.get("name", ""), "pdp_name": pdp["name"],
            "name_match": name_match,
            "api_price": api.get("price", ""), "catalogue_price": card.get("price", ""), "pdp_price": pdp["price"],
            "price_match": price_match,
            "api_brand": api.get("brand", ""), "pdp_brand": pdp["brand"],
            "brand_match": yn(clean(api.get("brand")) == pdp["brand"]) if api.get("brand") and pdp["brand"]
            else "not checked",
            "pdp_http_status": pdp_status or "failed",
            "main_image_url": img_url, "main_image_http_status": img_status or ("failed" if img_url else ""),
            "main_image_ok": yn(image_ok) if img_url else "not checked",
            "page_title": pdp["title"], "has_page_title": yn(pdp["title"]),
            "title_names_product": yn(product_name and product_name.lower() in pdp["title"].lower()),
            "h1_count": pdp["h1_count"], "has_h1": yn(pdp["h1_count"] > 0),
            "product_heading_tag": pdp["heading_tag"],
            "main_image_alt": pdp["image_alt"] if pdp["image_alt"] is not None else "(missing)",
            "has_alt": yn(has_alt),
            "alt_names_product": yn(has_alt and product_name.lower() in pdp["image_alt"].lower()),
            "checks_not_completed": "; ".join(not_done),
        }
        if pdp_status != 200:
            for key in ("has_page_title", "title_names_product", "has_h1", "has_alt", "alt_names_product"):
                row[key] = "not checked"

        failed = [label for key, label in (
            ("name_match", "name differs"), ("price_match", "price differs"), ("brand_match", "brand differs"),
            ("main_image_ok", "main image not loading"), ("has_page_title", "no page title"),
            ("title_names_product", "title not product-specific"), ("has_h1", "no h1"),
            ("has_alt", "no alt text"), ("alt_names_product", "alt not product-specific"),
        ) if row[key] == "N"]
        if pdp_status not in (200, None):
            failed.insert(0, f"product page HTTP {pdp_status}")
        row["facts_failed"] = "; ".join(failed)
        row["_pdp"] = pdp
        rows.append(row)

        flag = "OK" if not failed and not not_done else ("INCOMPLETE" if not_done else "ATTENTION")
        print(f"  {pid:>3}  {product_name[:38]:38}  name={name_match:<3} price={price_match:<3} "
              f"brand={row['brand_match']:<3} "
              f"page={row['pdp_http_status']} img={row['main_image_http_status']}  {flag}")

    # Alt text used on most products is treated as generic
    alts = [r["_pdp"]["image_alt"] for r in rows if r["_pdp"]["image_alt"]]
    generic_alts = {a for a in set(alts) if alts.count(a) > len(rows) / 2}
    for r in rows:
        r["content_review"] = content_review(clean(r["api_name"]), r.pop("_pdp"), generic_alts)
        r["attention"] = "INCOMPLETE" if r["checks_not_completed"] else ("YES" if r["facts_failed"] else "no")

    # 4. Site-wide checks
    site = []
    titles = {r["page_title"] for r in rows if r["page_title"]}
    if len(titles) == 1 and len(rows) > 1:
        site.append(f'All {len(rows)} product pages share one title: "{titles.pop()}"')
    if generic_alts:
        site.append(f'Main image alt text is the same generic text on most pages: "{", ".join(generic_alts)}"')
    probe_status, _, probe_page, _ = fetch(f"{BASE}/product_details/999999")
    if probe_status == 200 and not parse_product_page(probe_page)["name"]:
        site.append("A product id that does not exist (/product_details/999999) returns HTTP 200 with an empty "
                    "product template (soft 404) instead of 404 or a 'product not found' message")
    tshirt_spellings = sorted({m.group(0) for r in rows
                               for m in re.finditer(r"t[\s-]?shirt", r["api_name"], re.I)})
    if len(tshirt_spellings) > 1:
        site.append(f"Content: 'T-shirt' is spelled {len(tshirt_spellings)} ways across product names "
                    f"({', '.join(repr(s) for s in tshirt_spellings)}) - inconsistent for customers and site search")
    api_only = sorted(set(api_products) - set(catalogue))
    cat_only = sorted(set(catalogue) - set(api_products))
    if catalogue and api_only:
        site.append(f"In API but not on catalogue page: {api_only}")
    if cat_only:
        site.append(f"On catalogue page but not in API: {cat_only}")

    # 5. Write outputs
    csv_path = OUT_DIR / f"catalogue_{stamp}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:  # utf-8-sig so Excel shows Rs./dashes correctly
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    md_path = OUT_DIR / f"catalogue_{stamp}.md"
    md_path.write_text(summary_markdown(rows, site, checked_at, len(api_products), cat_status,
                                        len(catalogue), time.time() - started, csv_path.name),
                       encoding="utf-8")
    shutil.copyfile(csv_path, OUT_DIR / "latest.csv")
    shutil.copyfile(md_path, OUT_DIR / "latest.md")

    attention = sum(r["attention"] == "YES" for r in rows)
    incomplete = sum(r["attention"] == "INCOMPLETE" for r in rows)
    print(f"\nDone in {time.time() - started:.0f}s - {len(rows)} products, {attention} need attention, "
          f"{incomplete} incomplete")
    print(f"  {csv_path}\n  {md_path}")


def summary_markdown(rows, site, checked_at, api_count, cat_status, cat_count, seconds, csv_name):
    def count(key, value="N"):
        return sum(r[key] == value for r in rows)

    lines = [
        "# Catalogue Report",
        "",
        "Automatic check of every product. *Site-wide findings* = problems on every page. "
        "*Content to review* = opinion, not pass/fail.",
        "",
        "| Item | Detail |",
        "|---|---|",
        f"| Checked | {checked_at} |",
        f"| Site | {BASE} |",
        f"| Products checked | {len(rows)} (API: {api_count}, catalogue page: {cat_count}"
        f"{'' if cat_status == 200 else ' - catalogue page unavailable'}) |",
        f"| Run time | {seconds:.0f} s |",
        f"| Full data | `{csv_name}` (one row per product, opens in Excel) |",
        "| Generated by | `scripts/catalogue_audit.py` |",
        "",
        "## Factual checks",
        "",
        "| Check | Pass | Fail | Not checked |",
        "|---|---|---|---|",
    ]
    for key, label in (
        ("name_match", "Name agrees: API, catalogue page, product page"),
        ("price_match", "Price agrees: API, catalogue page, product page"),
        ("brand_match", "Brand agrees: API, product page"),
        ("main_image_ok", "Main image loads (HTTP 200, image type)"),
        ("has_page_title", "Page has a `<title>`"),
        ("title_names_product", "Title contains the product name"),
        ("has_h1", "Page has an `<h1>` primary heading"),
        ("has_alt", "Main image has alt text"),
        ("alt_names_product", "Alt text contains the product name"),
    ):
        lines.append(f"| {label} | {count(key, 'Y')} | {count(key, 'N')} | {count(key, 'not checked')} |")
    pdp_ok = sum(str(r["pdp_http_status"]) == "200" for r in rows)
    pdp_unreached = sum(r["pdp_http_status"] == "failed" for r in rows)
    lines += [f"| Product page loads (HTTP 200) | {pdp_ok} | {len(rows) - pdp_ok - pdp_unreached} | {pdp_unreached} |",
              ""]

    lines += ["## Site-wide findings", ""]
    lines += [f"- {s}" for s in site] or ["- None"]

    lines += ["", "## Products needing attention (factual)", ""]
    flagged = [r for r in rows if r["facts_failed"]]
    if flagged:
        common = set.intersection(*[set(r["facts_failed"].split("; ")) for r in flagged]) if len(flagged) > 1 else set()
        if common:
            ids = ", ".join(str(r["product_id"]) for r in flagged)
            lines.append(f"**{len(flagged)} of {len(rows)} products** fail the same checks: "
                         f"**{', '.join(sorted(common))}**. These are template issues - one fix covers all pages "
                         f"(see site-wide findings).")
            lines.append("")
            lines.append(f"Affected product IDs: {ids}. Per-product values are in the CSV.")
            lines.append("")
        extra = [(r, [f for f in r["facts_failed"].split("; ") if f not in common]) for r in flagged]
        extra = [(r, other) for r, other in extra if other]
        if extra:
            lines += ["| ID | Product | URL | Failed checks |", "|---|---|---|---|"]
            lines += [f"| {r['product_id']} | {r['api_name'] or r['pdp_name']} | {r['pdp_url']} | {', '.join(other)} |"
                      for r, other in extra]
        else:
            lines.append("No product has any other factual failure: names, prices, pages and images are all correct.")
    else:
        lines.append("None.")

    lines += ["", "## Content to review (judgement, not a pass/fail result)", ""]
    reviewed = [r for r in rows if r["content_review"]]
    generic = [n for n in ("Alt text is generic", "Page title does not name the product")]
    specific = []
    for r in reviewed:
        notes = [n for n in r["content_review"].split("; ") if not any(n.startswith(g) for g in generic)]
        if notes:
            specific.append(f"| {r['product_id']} | {r['api_name']} | {'; '.join(notes)} |")
    lines.append("Generic alt text and non-specific titles apply to every product (site-wide findings). "
                 "Product-specific points:")
    lines.append("")
    lines += ["| ID | Product | Note |", "|---|---|---|"] + specific if specific else ["None."]

    lines += ["", "## Checks not completed", ""]
    incomplete = [r for r in rows if r["checks_not_completed"]]
    lines += [f"- {r['product_id']} ({r['pdp_url']}): {r['checks_not_completed']}" for r in incomplete] \
        or ["None - every check ran for every product."]

    lines += ["", "## Method and limits", "",
              "- Name and price compared after collapsing whitespace and decoding HTML entities; "
              "price compared as a number (Rs. 1,000 = 1000).",
              "- Catalogue values come from the product cards on /products; product page values from the "
              "product information block; main image is the image in the product view block.",
              "- 'Contains the product name' is a factual string check; whether wording is *useful* is listed "
              "under Content to review.",
              "- One request at a time with a short pause; failed requests are retried twice and then reported "
              "under Checks not completed.",
              "- Only server HTML is checked (no JavaScript run). Content added by scripts after load is not covered.",
              ""]
    return align_tables("\n".join(lines))


def display_width(text):
    """Width of text as shown in a monospace editor (wide characters such as emoji count as 2)."""
    width = 0
    for ch in text:
        if unicodedata.combining(ch) or ch == "️":
            continue
        width += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return width


def align_tables(markdown):
    """Pad every Markdown table so its column borders line up in the raw .md file."""
    out, block = [], []

    def flush():
        if block:
            rows = [[c.strip() for c in line.strip().strip("|").split("|")] for line in block]
            widths = [max(display_width(r[i]) for r in rows if i < len(r)) for i in range(len(rows[0]))]
            widths = [max(w, 3) for w in widths]
            for n, r in enumerate(rows):
                if n == 1:
                    cells = ["-" * w for w in widths]
                else:
                    cells = [c + " " * (widths[i] - display_width(c)) for i, c in enumerate(r)]
                out.append("| " + " | ".join(cells) + " |")
            block.clear()

    for line in markdown.split("\n"):
        if line.startswith("|"):
            block.append(line)
        else:
            flush()
            out.append(line)
    flush()
    return "\n".join(out)


if __name__ == "__main__":
    main()
