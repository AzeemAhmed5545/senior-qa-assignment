# Test Record (§5)

Every test that was run: input, expected result (and why), actual result, evidence.

**Setup:** https://automationexercise.com · Chrome 156 · Windows 11 · desktop 1440×900 · mobile
375×667 · own test account · no order placed

**Basis** (why that result was expected): Brief · Docs = API docs · WCAG 2.2 · Site = site's own
rule · Heuristic = usability good practice

## Summary — 53 tests

| Section         | Tests  | Pass   | Pass (to review) | Fail   |
| --------------- | ------ | ------ | ---------------- | ------ |
| A. Journey      | 28     | 16     | 2                | 10     |
| B. API          | 6      | 6      | 0                | 0      |
| C. Consistency  | 3      | 3      | 0                | 0      |
| D. Technical    | 2      | 0      | 0                | 2      |
| E. Frontend fix | 8      | 8      | 0                | 0      |
| F. Catalogue    | 6      | 5      | 0                | 1      |
| **Total**       | **53** | **38** | **2**            | **13** |

Every FAIL links to a defect (DEF) or improvement (IMP). Nothing was blocked.

## A. Customer journey (29 Oct; TR-17 and TR-28 on 30 Oct)

Evidence: `evidence/desktop/` (desktop), `evidence/mobile/` (mobile), `evidence/technical/`

| ID    | Test                             | Expected (basis)                  | Actual                                       | Status        | Evidence                               | Ref    |
| ----- | -------------------------------- | --------------------------------- | -------------------------------------------- | ------------- | -------------------------------------- | ------ |
| TR-01 | Search `top`                     | 14 results (Docs)                 | 14, Blue Top first                           | PASS          | `01-search-top-1440.png`               |        |
| TR-02 | Search `zzzznotfound123`         | "No products" message (Heuristic) | Empty area, no message                       | FAIL          | `02-search-no-match-1440.png`          | DEF-04 |
| TR-03 | Open Blue Top                    | Details match API (Docs)          | All match                                    | PASS          | `03-pdp-qty2-1440.png`                 |        |
| TR-04 | Quantity `2`                     | Accepted (Brief)                  | Accepted                                     | PASS          | `03-pdp-qty2-1440.png`                 |        |
| TR-05 | Add to cart                      | Confirmation (Brief)              | "Added!" + View Cart                         | PASS          | `04-add-to-cart-modal-1440.png`        |        |
| TR-06 | Cart total                       | 2 × 500 = 1000                    | Rs. 1000                                     | PASS          | `05-cart-qty2-1440.png`                |        |
| TR-07 | Add Men Tshirt                   | 2 rows, 1000 + 400                | Correct                                      | PASS          | `06-cart-two-products-1440.png`        |        |
| TR-08 | Remove Men Tshirt                | Row gone, 1000 left (Brief)       | Correct                                      | PASS          | `07-cart-after-remove-1440.png`        |        |
| TR-09 | Remove all                       | Empty-cart message                | "Cart is empty!"                             | PASS          | `14-cart-empty-1440.png`               |        |
| TR-10 | Quantity `0`                     | Rejected (Site `min=1`)           | Added, Rs. 0                                 | FAIL          | `13-invalid-qty-0-1440.png`            | DEF-01 |
| TR-11 | Quantity `-1`                    | Rejected (Site `min=1`)           | Added, **Rs. −500**                          | FAIL          | `13-invalid-qty-minus1-1440.png`       | DEF-01 |
| TR-12 | Quantity blank                   | Rejected with message (Heuristic) | Not added, but no message                    | PASS (review) | `15-qty-blank-rejected-1440.png`       | demo   |
| TR-13 | Quantity `999`                   | Accepted — no limit documented    | Accepted, Rs. 499,500                        | PASS          | `16-qty-999-accepted-1440.png`         | IMP-01 |
| TR-14 | Checkout logged out              | Login prompt (Brief)              | Prompt; cart kept                            | PASS          | `08-checkout-login-gate-1440.png`      |        |
| TR-15 | Register test account            | Account created (Brief)           | Created, logged in                           | PASS          | `10-account-created-1440.png`          |        |
| TR-16 | Checkout logged in               | Review with total (Brief)         | Rs. 1000 shown                               | PASS          | `11-checkout-review-1440.png`          |        |
| TR-17 | Tab to search field, then button | Visible focus (WCAG 2.4.7)        | Field OK; button 1.19:1, invisible           | FAIL          | `focus-2-search-button-tab.png`        | DEF-08 |
| TR-18 | `top` + Enter                    | Search runs (WCAG 2.1.1)          | Nothing happens                              | FAIL          | `12-keyboard-enter-no-search-1440.png` | DEF-07 |
| TR-19 | Tab to button + Space            | Search runs                       | 14 results                                   | PASS          | `01-search-top-1440.png`               |        |
| TR-20 | Search button name               | Has a name (WCAG 4.1.2)           | `button ""`                                  | FAIL          | `a11y-tree-search-control.yml`         | DEF-02 |
| TR-21 | Quantity field name              | "Quantity" (WCAG 1.3.1)           | No name                                      | FAIL          | `a11y-tree-quantity-field.yml`         | DEF-03 |
| TR-22 | Mobile: search `top`             | 14 results, fits screen           | 14, fits                                     | PASS          | `iphone-se-search.png`                 |        |
| TR-23 | Mobile: no-match search          | Message (Heuristic)               | No message                                   | FAIL          | `iphone-se-search-no-match.png`        | DEF-04 |
| TR-24 | Mobile: add qty 2, view cart     | Total visible                     | Total correct but **off-screen** until swipe | PASS (review) | `iphone-se-cart.png`                   | IMP-09 |
| TR-25 | Mobile: checkout review          | Readable                          | Rs. 1000, fits                               | PASS          | `iphone-se-checkout.png`               |        |
| TR-26 | Product page title               | Names product (WCAG 2.4.2)        | Same on every page                           | FAIL          | `03-pdp-qty2-1440.png`                 | DEF-05 |
| TR-27 | Main image alt                   | Describes product (WCAG 1.1.1)    | "ecommerce website products"                 | FAIL          | `03-pdp-qty2-1440.png`                 | DEF-06 |
| TR-28 | Mobile: remove one of two items  | Item removed (Brief)              | Works after swiping table; Blue Top left     | PASS          | `iphone-se-cart-after-remove.png`      | IMP-09 |

**Changed after re-checking:** TR-13 FAIL → PASS (no limit is documented) · TR-17 narrowed to the
button (field is fine) · TR-24 PASS → to review (screenshot shows total cut off).

## B. API — product search (30 Oct)

Tool: Postman + curl · Evidence: `evidence/api/` · Details:
[`findings/API_CHECKS.md`](../findings/API_CHECKS.md)

| ID     | Request                          | Expected (basis)           | Actual                     | Status | Ref    |
| ------ | -------------------------------- | -------------------------- | -------------------------- | ------ | ------ |
| API-A1 | `search_product=top`             | Code 200 + list (Docs)     | HTTP 200, 14 products      | PASS   |        |
| API-A2 | `search_product=zzzznotfound123` | Empty list (not in docs)   | HTTP 200, `products: []`   | PASS   |        |
| API-A3 | Parameter missing                | Code 400 + message (Docs)  | HTTP **200**, body **400** | PASS   | AMB-01 |
| API-A4 | Blank value (extra)              | Not in docs                | HTTP 200, all 34 products  | PASS   | IMP-05 |
| API-A5 | `GET` (extra)                    | Rejected (Docs: POST only) | HTTP 200, body 405         | PASS   |        |
| API-A6 | Wrong parameter name (extra)     | Code 400 (Docs)            | HTTP 200, body 400         | PASS   | AMB-01 |

## C. Data consistency

| ID     | Check                                       | Actual                        | Status | Evidence                               |
| ------ | ------------------------------------------- | ----------------------------- | ------ | -------------------------------------- |
| CON-01 | Blue Top in API, search, product page, cart | Rs. 500 everywhere; cart 1000 | PASS   | `findings/TECHNICAL_ASSESSMENT.md`     |
| CON-02 | "top" count: page vs API                    | 14 = 14                       | PASS   | `01-search-top-1440.png`, `A1-raw.txt` |
| CON-03 | Name and price, all products, 3 sources     | 34/34 agree                   | PASS   | `catalogue/reports/latest.csv`         |

## D. Technical (30 Oct)

| ID     | Check                         | Expected  | Actual                     | Status | Ref    |
| ------ | ----------------------------- | --------- | -------------------------- | ------ | ------ |
| TEC-01 | Console on product page       | No errors | 3 errors; fonts never load | FAIL   | DEF-11 |
| TEC-02 | Product ID that doesn't exist | HTTP 404  | HTTP 200, empty page       | FAIL   | DEF-10 |

Evidence: `evidence/technical/console-mixed-content-fonts.txt`, `soft-404-product-999999.txt`

## E. Frontend fix — quantity field (30 Oct)

Evidence: `frontend-demo/evidence/` · Details:
[`frontend-demo/README.md`](../frontend-demo/README.md)

| ID    | Check                             | Actual                                     | Status |
| ----- | --------------------------------- | ------------------------------------------ | ------ |
| FE-01 | Before: qty 0                     | Request sent, "Added!" (defect reproduced) | PASS   |
| FE-02 | After: qty 0                      | Blocked with message                       | PASS   |
| FE-03 | After: −1, blank, 1.5, 1e2, space | All blocked, 0 requests                    | PASS   |
| FE-04 | After: field name                 | "Quantity:"                                | PASS   |
| FE-05 | Regression: qty 2 by keyboard     | Added as before                            | PASS   |
| FE-06 | Regression: cart total            | Rs. 1000, one row                          | PASS   |
| FE-07 | Product 2 at 375px                | Blocked, fits screen                       | PASS   |
| FE-08 | Local demo                        | 0 blocked, 2 sent                          | PASS   |

## F. Catalogue report (30 Oct)

Details: [`catalogue/README.md`](../catalogue/README.md)

| ID     | Check                                      | Actual                            | Status | Ref                    |
| ------ | ------------------------------------------ | --------------------------------- | ------ | ---------------------- |
| CAT-01 | Name and price agree, every product        | 34/34                             | PASS   |                        |
| CAT-02 | Page and main image load, every product    | 34/34                             | PASS   |                        |
| CAT-03 | Title, `<h1>`, alt specific to the product | Generic on 34/34; no `<h1>` on 34 | FAIL   | DEF-05, DEF-06, IMP-02 |
| CAT-04 | Script vs manual check (#23, #43)          | Identical                         | PASS   |                        |
| CAT-05 | Self-check with injected faults            | 5/5                               | PASS   |                        |
| CAT-06 | Refresh time                               | About 60 s (limit 5 min)          | PASS   |                        |

## Not tested

Payment · screen readers · browsers other than Chrome · tablets · browsing by category · load and
security.
