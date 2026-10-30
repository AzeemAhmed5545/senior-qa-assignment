# Senior QA Assignment — Automation Exercise

QA review of **https://automationexercise.com** for the Senior QA Engineer assignment: customer
journey, search API and full product catalogue.

## At a glance

| Item         | Result                                                      |
| ------------ | ----------------------------------------------------------- |
| Dates        | 29–30 Oct 2026                                              |
| Browser      | Chrome 156 (Windows 11) · desktop 1440×900 · mobile 375×667 |
| Tests        | 53 → 38 pass · 2 pass (to review) · 13 fail                 |
| Defects      | 10 confirmed (0 critical · 6 major · 4 minor) · 1 withdrawn |
| Improvements | 9 suggestions (not defects)                                 |
| Catalogue    | 34 products checked in about 1 minute                       |

## Verdict

- ✅ Search → product → cart → checkout works on desktop and mobile. Prices and totals are correct.
- ❌ **Fix first:** quantity 0 or −1 is accepted and says "Added!" (cart can show **Rs. −500**).
- ⚠️ Keyboard and screen-reader users struggle: unnamed controls, same title on every product page.
- ⚠️ On mobile, cart totals and the remove button are hidden until you swipe the table.

## Start here

| Brief | Open                                                                   | What you get                                    |
| ----- | ---------------------------------------------------------------------- | ----------------------------------------------- |
| §1    | [`findings/FINDINGS.md`](findings/FINDINGS.md)                         | 13 findings in priority order + what works well |
| §2    | [`findings/TECHNICAL_ASSESSMENT.md`](findings/TECHNICAL_ASSESSMENT.md) | The "top" journey checked in depth              |
| §2    | [`findings/API_CHECKS.md`](findings/API_CHECKS.md)                     | Search API: 6 requests and results              |
| §3    | [`frontend-demo/README.md`](frontend-demo/README.md)                   | Quantity field fix, before/after                |
| §4    | [`catalogue/reports/latest.md`](catalogue/reports/latest.md)           | Every product checked                           |
| §4    | [`catalogue/README.md`](catalogue/README.md)                           | How to refresh the report                       |
| §5    | [`tests/TEST_RECORD.md`](tests/TEST_RECORD.md)                         | All 53 tests with evidence                      |
| §5    | [`defects/DEFECTS.md`](defects/DEFECTS.md)                             | 10 developer-ready defects                      |
| §5    | [`findings/IMPROVEMENTS.md`](findings/IMPROVEMENTS.md)                 | 9 suggestions                                   |
| §6    | [`findings/RECOMMENDATION.md`](findings/RECOMMENDATION.md)             | Ready for customers? What to fix first?         |
| —     | [`AI_USAGE.md`](AI_USAGE.md)                                           | Tools and how AI output was checked             |

## Run it yourself

Needs only **Python 3.8+** and a browser.

| What                    | How                                                                                      |
| ----------------------- | ---------------------------------------------------------------------------------------- |
| Catalogue report        | `python scripts/catalogue_audit.py` → open `catalogue/reports/latest.md` (≈ 1 min)       |
| Check the script itself | `python scripts/catalogue_audit_selfcheck.py` → expect 5 × PASS                          |
| API tests               | Postman → Import `api/AutomationExercise-SearchProduct.postman_collection.json` → Run    |
| Frontend fix (live)     | Open a product page → F12 Console → paste `frontend-demo/improvement.js`                 |
| Frontend fix (local)    | `cd frontend-demo && python -m http.server 8765` → open `localhost:8765/local-demo.html` |

## Tools used

| Tool             | Used for                                                      |
| ---------------- | ------------------------------------------------------------- |
| Claude Code (AI) | Planning, scripts, first drafts — every result was checked    |
| Playwright MCP   | Let the AI drive Chrome: screenshots, keyboard, accessibility |
| Postman          | API tests (6 requests, 18 checks)                             |
| curl             | Raw API responses and page source                             |
| Python           | Catalogue script and its self-check                           |
| Chrome DevTools  | Manual checks of markup and console                           |

## Time spent

| Date      | Work                                                     | Hours  |
| --------- | -------------------------------------------------------- | ------ |
| 27–28 Oct | Brief, site exploration, first notes                     | 9.0    |
| 29 Oct    | Customer journey on desktop and mobile, first defects    | 1.5    |
| 30 Oct    | API, technical checks, frontend fix, catalogue, write-up | 4.5    |
| **Total** | Actual, with AI help                                     | **15** |

Done fully by hand, this would take about **21 hours**. AI saved time on writing, not on checking.

## Assumptions and limits

| Assumption / limit                                                                |
| --------------------------------------------------------------------------------- |
| One mobile size (375×667) and one browser (Chrome)                                |
| Stopped at checkout review — **no order or payment**                              |
| Quantity below 1 is invalid (site's own `min="1"`); no maximum is documented      |
| API "Response Code: 400" may mean HTTP status or body field — reported as unclear |
| No screen reader, load or security testing                                        |
| Own throwaway test account only (`qa.azim+ae1@example.com`, no real data)         |

## Ready for the review

| Task                          | Status                                                         |
| ----------------------------- | -------------------------------------------------------------- |
| Refresh catalogue (≤ 5 min)   | ✅ Practised: about 60 s                                       |
| Small live change (10–15 min) | ✅ Practised: "add brand check" done and checked in 4 min 08 s |
