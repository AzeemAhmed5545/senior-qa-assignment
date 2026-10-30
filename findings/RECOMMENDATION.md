# Recommendation (§6)

Based on 53 tests, 6 API checks, all 34 products and a working frontend fix · Chrome only · 29–30
Oct.

## 1. Ready for customers?

**Yes for most customers — with one condition.**

| Who / what                     | Verdict                                                                                 |
| ------------------------------ | --------------------------------------------------------------------------------------- |
| Mouse or touch users           | ✅ Search, cart and checkout work; prices and totals correct; nothing blocks a purchase |
| Quantity field                 | ❌ 0 and −1 are accepted (cart can show **Rs. −500**) — main risk until fixed           |
| Keyboard / screen-reader users | ⚠️ Can get through, but with real difficulty (unnamed controls, same titles)            |
| Phone users                    | ⚠️ Cart totals and Remove are hidden until you swipe the table                          |

## 2. Fix first

| #   | Fix                                                    | Why                                            | Effort     |
| --- | ------------------------------------------------------ | ---------------------------------------------- | ---------- |
| 1   | DEF-01 — validate quantity ≥ 1 (client **and** server) | Only issue affecting money. Fix already demoed | Small      |
| 2   | DEF-02/03 — name the search button and quantity field  | Two attributes; unblocks screen-reader users   | Very small |
| 3   | DEF-04 — "no products found" message                   | Dead end on the main entry point               | Small      |
| 4   | DEF-05/06 — product name in title and image alt        | One template change fixes 34 pages             | Small      |

## 3. Can wait

| When             | Items                                                                                                           |
| ---------------- | --------------------------------------------------------------------------------------------------------------- |
| Next sprint (P2) | DEF-07 Enter key · DEF-08 focus ring · DEF-10 404 page · IMP-09 mobile cart · IMP-02 `<h1>` · IMP-04 API status |
| Backlog (P3/P4)  | DEF-11 fonts · IMP-01, 03, 05, 06, 07, 08                                                                       |

## 4. Not known / not tested

| Area                                  | Why it matters                                     |
| ------------------------------------- | -------------------------------------------------- |
| Payment and order confirmation        | Could a negative quantity be charged? Unknown      |
| Server-side quantity rules            | Server accepts qty 0; needs code access to confirm |
| Screen readers                        | Real announcements unverified                      |
| Firefox, Safari, tablets, real phones | Layout may differ                                  |
| API error design (AMB-01)             | Needs the API owner to say what was intended       |

This was a focused review — **not proof the whole site is defect-free.**

## 5. Re-test after a change

| After fixing      | Re-check                                                                       |
| ----------------- | ------------------------------------------------------------------------------ |
| Quantity (DEF-01) | 0, −1, blank rejected · 2 adds · cart Rs. 1000 · direct URL with −1 rejected   |
| Search and labels | Names in DevTools · Enter searches · focus visible (TR-17 to TR-21)            |
| Templates         | `python scripts/catalogue_audit.py` → every product passes                     |
| API               | Run the Postman collection (18 checks)                                         |
| **Any change**    | Search "top" = 14 · Blue Top Rs. 500 · cart total · remove · checkout · mobile |

## 6. Keep the checks useful

- Run the catalogue audit nightly or before each release — new products are picked up automatically.
- Run the Postman collection in CI on every API change.
- Turn the §5 regression list into Playwright tests (desktop + 375px), with accessibility checks.
- Update the docs once open questions are decided (AMB-01, blank search, search rules).
