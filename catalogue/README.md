# Catalogue Report (§4)

One command checks **every product** on the site and writes a dated report.

**Latest report:** [`reports/latest.md`](reports/latest.md) (summary) · `reports/latest.csv` (all
values, opens in Excel)

## Refresh in under 5 minutes

1. Open a terminal in the project folder.
2. Run `python scripts/catalogue_audit.py` (about 60 seconds, needs only Python 3.8+).
3. Open `catalogue/reports/latest.md` — check the **Checked** time is now.

Older runs stay in `reports/` with their timestamp. Failed requests are retried twice, then listed
under **Checks not completed** — never hidden or counted as a pass.

## Result (30 Oct)

| Check                                            | Result                                   |
| ------------------------------------------------ | ---------------------------------------- |
| Name, price agree (API, catalogue, product page) | ✅ 34/34                                 |
| Brand agrees (API, product page)                 | ✅ 34/34                                 |
| Product page and main image load                 | ✅ 34/34                                 |
| Page title names the product                     | ❌ 0/34 — same title everywhere (DEF-05) |
| Page has an `<h1>`                               | ❌ 0/34 (IMP-02)                         |
| Image alt names the product                      | ❌ 0/34 — generic text (DEF-06)          |
| Missing product ID gives 404                     | ❌ returns 200, empty page (DEF-10)      |

**Content to review (opinion, not pass/fail):** "T-shirt" spelled 3 ways; #22, #24, #43 naming; #23
long name.

## What each CSV column means

| Columns                                     | Meaning                                                  |
| ------------------------------------------- | -------------------------------------------------------- |
| `api_*`, `catalogue_*`, `pdp_*`             | Value from the API, the /products page, the product page |
| `name_match`, `price_match`, `brand_match`  | Y / N / not checked                                      |
| `pdp_http_status`, `main_image_http_status` | Page and image HTTP status                               |
| `has_page_title`, `has_h1`, `has_alt`       | Present or not (fact)                                    |
| `title_names_product`, `alt_names_product`  | Contains the product name (fact)                         |
| `facts_failed`                              | Which factual checks failed                              |
| `content_review`                            | Wording points (opinion)                                 |
| `checks_not_completed`                      | Anything that couldn't be checked, and why               |
| `attention`                                 | YES / no / INCOMPLETE                                    |

## How the script was verified

| Check                                                                                        | Result               |
| -------------------------------------------------------------------------------------------- | -------------------- |
| Products #23 and #43 compared by hand                                                        | Identical to the CSV |
| `python scripts/catalogue_audit_selfcheck.py` (injects a timeout, wrong price, broken image) | 5/5 PASS             |
| Timed refresh                                                                                | 63 s                 |

## Live-change practice

Request: _"Also check that the brand matches."_ → about 12 lines added → run → checked by hand →
self-check 5/5. **Done in 4 min 08 s** (about 10–12 min by hand).

## Limits

Server HTML only (no JavaScript) · "accessible" image = loads with HTTP 200 · category and stock not
compared · ≈ 70 read-only requests, one at a time (not a load test).
