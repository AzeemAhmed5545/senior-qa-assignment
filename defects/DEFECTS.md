# Defects (§5)

Confirmed bugs only, each ready for a developer to reproduce, fix and re-test. Suggestions are in
[`findings/IMPROVEMENTS.md`](../findings/IMPROVEMENTS.md).

**Severity:** S1 critical (blocks purchase) · S2 major (wrong result / users badly affected) · S3
minor

**Priority:** P1 next sprint · P2 soon · P3 backlog

**Environment:** Windows 11 · Chrome 156.0.8078.48 (29 Oct) / 156.0.8078.74 (30 Oct) · live site

## Summary — 10 defects (0 × S1 · 6 × S2 · 4 × S3)

| ID         | Defect                                            | Area          | Sev | Pri |
| ---------- | ------------------------------------------------- | ------------- | --- | --- |
| DEF-01     | Quantity accepts 0 and negative values            | Functional    | S2  | P1  |
| DEF-02     | Search button has no accessible name              | Accessibility | S2  | P1  |
| DEF-03     | Quantity field has no accessible name             | Accessibility | S2  | P1  |
| DEF-04     | No message when a search finds nothing            | Usability     | S2  | P1  |
| DEF-05     | Same page title on every product page             | Access. / SEO | S2  | P1  |
| DEF-06     | Generic image alt text on every product           | Accessibility | S2  | P1  |
| DEF-07     | Enter key doesn't start a search                  | Accessibility | S3  | P2  |
| DEF-08     | Search button focus is too faint to see           | Accessibility | S3  | P2  |
| ~~DEF-09~~ | ~~No maximum quantity~~ — withdrawn, now IMP-01   | —             | —   | —   |
| DEF-10     | Missing product shows an empty page with HTTP 200 | Functional    | S3  | P2  |
| DEF-11     | Site fonts blocked (loaded over `http://`)        | Visual        | S3  | P3  |

---

## DEF-01 · Quantity accepts 0 and negative values · S2 / P1

|          |                                                                                                |
| -------- | ---------------------------------------------------------------------------------------------- |
| Where    | `/product_details/1` · 29 Oct                                                                  |
| Steps    | 1) Type `0` in Quantity 2) Click **Add to cart** 3) Open `/view_cart` 4) Repeat with `-1`      |
| Expected | Rejected (the field has `min="1"`)                                                             |
| Actual   | "Added!" shown. Cart: qty 0 = Rs. 0, qty −1 = **Rs. −500**                                     |
| Evidence | `evidence/desktop/13-invalid-qty-0-1440.png`, `13-invalid-qty-minus1-1440.png`                 |
| Why      | Negative totals can corrupt order value and reporting                                          |
| Cause    | `cart.js` sends the value unchecked; server also accepts `GET /add_to_cart/1?quantity=0` (200) |
| Fix      | Validate `quantity ≥ 1` in `cart.js` **and** on the server. Demo: `frontend-demo/`             |
| Re-test  | 0, −1, blank rejected with a message; cart never shows qty < 1                                 |

## DEF-02 · Search button has no accessible name · S2 / P1

|          |                                                                       |
| -------- | --------------------------------------------------------------------- |
| Where    | `/products` · `#submit_search`                                        |
| Steps    | Inspect the magnifier button → DevTools Accessibility pane            |
| Expected | Name "Search products" (WCAG 4.1.2)                                   |
| Actual   | Empty name: `button ""` — icon only, no text, `aria-label` or `title` |
| Evidence | `evidence/technical/a11y-tree-search-control.yml`                     |
| Why      | Screen-reader users hear just "button"                                |
| Fix      | `aria-label="Search products"`                                        |
| Re-test  | Accessibility pane shows the name                                     |

## DEF-03 · Quantity field has no accessible name · S2 / P1

|          |                                                                  |
| -------- | ---------------------------------------------------------------- |
| Where    | `/product_details/1` · `#quantity`                               |
| Steps    | Inspect the "Quantity:" label and the input → Accessibility pane |
| Expected | Field announced as "Quantity" (WCAG 1.3.1, 4.1.2)                |
| Actual   | `<label>` has no `for`; field is an unnamed `spinbutton: "1"`    |
| Evidence | `evidence/technical/a11y-tree-quantity-field.yml`                |
| Why      | Screen-reader users can't tell what the field changes            |
| Fix      | `<label for="quantity">Quantity:</label>`                        |
| Re-test  | Name is "Quantity"; clicking the label focuses the field         |

## DEF-04 · No message when a search finds nothing · S2 / P1

|          |                                                                                                 |
| -------- | ----------------------------------------------------------------------------------------------- |
| Where    | `/products?search=zzzznotfound123` · desktop and mobile                                         |
| Steps    | Search `zzzznotfound123`                                                                        |
| Expected | A "no products found" message and a way back (usability heuristic)                              |
| Actual   | "SEARCHED PRODUCTS" heading, then empty space                                                   |
| Evidence | `evidence/desktop/02-search-no-match-1440.png`, `evidence/mobile/iphone-se-search-no-match.png` |
| Why      | Dead end — user can't tell what happened                                                        |
| Fix      | Show the searched term + "No products found" + link to all products                             |
| Re-test  | Message shows on desktop and 375px                                                              |

## DEF-05 · Same page title on every product page · S2 / P1

|          |                                                                                   |
| -------- | --------------------------------------------------------------------------------- |
| Where    | All 34 product pages                                                              |
| Steps    | Open `/product_details/1` and `/product_details/2`; compare tab titles            |
| Expected | Product-specific, e.g. `Blue Top - Product Details` (WCAG 2.4.2)                  |
| Actual   | Always `Automation Exercise - Product Details`                                    |
| Evidence | `evidence/desktop/03-pdp-qty2-1440.png`, `catalogue/reports/latest.md`            |
| Why      | Tabs and search results can't be told apart; weak SEO                             |
| Fix      | Build the title from the product name in the template                             |
| Re-test  | `python scripts/catalogue_audit.py` → "Title contains the product name" = 34 pass |

## DEF-06 · Generic image alt text on every product · S2 / P1

|          |                                                                             |
| -------- | --------------------------------------------------------------------------- |
| Where    | All 34 product pages (main image, badges, rating stars)                     |
| Expected | Main image `alt="Blue Top"`; decorative images `alt=""` (WCAG 1.1.1)        |
| Actual   | Always `alt="ecommerce website products"`                                   |
| Evidence | `evidence/desktop/03-pdp-qty2-1440.png`, `catalogue/reports/latest.md`      |
| Why      | Screen-reader users can't identify the product; decorative images add noise |
| Fix      | Use the product name for the main image; empty alt for decorative ones      |
| Re-test  | Catalogue audit → "Alt text contains the product name" = 34 pass            |

## DEF-07 · Enter key doesn't start a search · S3 / P2

|          |                                                         |
| -------- | ------------------------------------------------------- |
| Where    | `/products` search box                                  |
| Steps    | Type `top`, press **Enter**                             |
| Expected | Search runs (WCAG 2.1.1)                                |
| Actual   | Nothing happens — only the magnifier click works        |
| Evidence | `evidence/desktop/12-keyboard-enter-no-search-1440.png` |
| Cause    | Click-only handler; no `<form>`                         |
| Fix      | Wrap the search in a `<form>` and handle submit         |
| Re-test  | Enter and the button both go to `?search=top`           |

## DEF-08 · Search button focus is too faint to see · S3 / P2

|          |                                                                                                  |
| -------- | ------------------------------------------------------------------------------------------------ |
| Where    | `/products` · `#submit_search` · 30 Oct                                                          |
| Steps    | Click the sale banner above search → **Tab** (field) → **Tab** (button)                          |
| Expected | Clearly visible focus, ≥ 3:1 against unfocused (WCAG 2.4.7, 1.4.11)                              |
| Actual   | `outline: none`; only white → light grey (**1.19:1**). The field's blue border is fine           |
| Evidence | `evidence/technical/focus-1-search-field-tab.png`, `focus-2-search-button-tab.png`               |
| Fix      | `#submit_search:focus-visible { outline: 2px solid #fe980f; outline-offset: 2px; }`              |
| Re-test  | Tab to the button → clear orange ring                                                            |
| Note     | First version also blamed the field; re-test showed the field is fine, so narrowed to the button |

## DEF-09 · Withdrawn

No maximum quantity is documented, so accepting 999 breaks no rule. Moved to **IMP-01**.

## DEF-10 · Missing product shows an empty page with HTTP 200 · S3 / P2

|          |                                                                                |
| -------- | ------------------------------------------------------------------------------ |
| Where    | `/product_details/999999` (any ID that doesn't exist)                          |
| Steps    | `curl -s -i https://automationexercise.com/product_details/999999`             |
| Expected | HTTP 404 and a "product not found" message                                     |
| Actual   | HTTP **200**; blank name and price, broken image link, Add to cart still shown |
| Evidence | `evidence/technical/soft-404-product-999999.txt`                               |
| Why      | Old links land on a broken page; search engines may index empty pages          |
| Fix      | Return 404 with a not-found page and links to Products                         |
| Re-test  | 999999 → 404; real product → 200; catalogue audit no longer lists the soft 404 |

## DEF-11 · Site fonts blocked · S3 / P3

|          |                                                                                                      |
| -------- | ---------------------------------------------------------------------------------------------------- |
| Where    | Every page (`static/css/main.css`)                                                                   |
| Steps    | Open any page with DevTools Console; look at `main.css` lines 5–7                                    |
| Expected | Roboto, Open Sans and Abel load; no console errors                                                   |
| Actual   | 3 "Mixed Content … blocked" errors; `@import url(http://fonts.googleapis.com/…)`; default font shown |
| Evidence | `evidence/technical/console-mixed-content-fonts.txt`                                                 |
| Why      | Site doesn't look as designed; error noise hides real problems                                       |
| Fix      | Change the three imports to `https://`                                                               |
| Re-test  | No console errors; DevTools "Rendered fonts" shows Roboto                                            |
