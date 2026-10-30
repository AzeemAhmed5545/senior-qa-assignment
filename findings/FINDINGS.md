# Customer Journey Findings (§1)

What a customer experiences, in priority order. Desktop 1440×900 and mobile 375×667, Chrome, 29–30
Oct.

**Type:** Defect = breaks a rule or standard · Usability = works but confusing · Preference = taste

**Priority:** P1 fix next · P2 soon · P3 backlog · P4 nice to have

## Overview

| #   | Finding                                                     | Type       | Priority | Ref            |
| --- | ----------------------------------------------------------- | ---------- | -------- | -------------- |
| F1  | Quantity 0 or −1 is added and says "Added!"                 | Defect     | **P1**   | DEF-01         |
| F2  | Search button and quantity field have no screen-reader name | Defect     | **P1**   | DEF-02, DEF-03 |
| F3  | Search with no results shows a blank area                   | Defect     | **P1**   | DEF-04         |
| F4  | Every product page has the same title and image text        | Defect     | **P1**   | DEF-05, DEF-06 |
| F5  | Enter doesn't search; search button focus is invisible      | Defect     | P2       | DEF-07, DEF-08 |
| F6  | Missing product shows an empty page                         | Defect     | P2       | DEF-10         |
| F7  | Site fonts don't load                                       | Defect     | P3       | DEF-11         |
| F8  | Mobile cart: totals and remove button hidden off-screen     | Usability  | P2       | IMP-09         |
| F9  | Search matches categories too, with no result count         | Usability  | P3       | IMP-03         |
| F10 | Search box has no label (placeholder only)                  | Usability  | P3       | IMP-07         |
| F11 | No upper limit on quantity                                  | Usability  | P3       | IMP-01         |
| F12 | Product names written inconsistently                        | Preference | P3       | IMP-06         |
| F13 | Footer says "Copyright © 2021"                             | Preference | P4       | IMP-08         |

## Defects

### F1 · Quantity 0 or −1 is added · P1

|      |                                                                                                     |
| ---- | --------------------------------------------------------------------------------------------------- |
| Goal | Choose how many to buy                                                                              |
| Seen | `0` or `-1` → "Added!" → cart shows Rs. 0 or **Rs. −500** (`evidence/desktop/13-invalid-qty-*.png`) |
| Why  | False confirmation; a negative total can corrupt the order value                                    |
| Fix  | Show _"Enter a quantity of 1 or more."_ and add nothing. **Working demo:** `frontend-demo/`         |

### F2 · Controls have no screen-reader name · P1

|      |                                                                                                   |
| ---- | ------------------------------------------------------------------------------------------------- |
| Goal | Search and set a quantity with a screen reader                                                    |
| Seen | Search button = `button ""`; quantity = unnamed spinbutton (`evidence/technical/a11y-tree-*.yml`) |
| Why  | Both are on the purchase path; users can't tell what they do (WCAG 4.1.2, 1.3.1)                  |
| Fix  | `aria-label="Search products"` on the button; `<label for="quantity">` on the field               |

### F3 · No-results search is blank · P1

|      |                                                                                              |
| ---- | -------------------------------------------------------------------------------------------- |
| Goal | Find a product, or recover from a typo                                                       |
| Seen | `zzzznotfound123` → heading and empty space, desktop and mobile (`evidence/desktop/02-…png`) |
| Why  | Dead end: did it fail, load, or find nothing?                                                |
| Fix  | _"No products match 'zzzznotfound123'. Check the spelling or browse all products."_          |

### F4 · All product pages look the same · P1

|      |                                                                                                  |
| ---- | ------------------------------------------------------------------------------------------------ |
| Goal | Tell product tabs apart; understand the image with a screen reader                               |
| Seen | 34/34 pages: title _"Automation Exercise - Product Details"_, alt _"ecommerce website products"_ |
| Why  | Tabs, bookmarks and search results all look identical (WCAG 2.4.2, 1.1.1; SEO)                   |
| Fix  | One template change: title `Blue Top – Rs. 500 · Automation Exercise`, image `alt="Blue Top"`    |

### F5 · Keyboard search is hard · P2

|      |                                                                                                        |
| ---- | ------------------------------------------------------------------------------------------------------ |
| Goal | Search with the keyboard only                                                                          |
| Seen | Enter does nothing; Tab to the button shows almost no change (1.19:1) (`evidence/technical/focus-2-…`) |
| Why  | The only keyboard route is invisible (WCAG 2.1.1, 2.4.7, 1.4.11)                                       |
| Fix  | Wrap search in a `<form>`; add `#submit_search:focus-visible { outline: 2px solid #fe980f; }`          |

### F6 · Missing product shows an empty page · P2

|      |                                                                                |
| ---- | ------------------------------------------------------------------------------ |
| Goal | Open an old or shared product link                                             |
| Seen | `/product_details/999999` → HTTP 200, blank name and price, broken image       |
| Why  | Looks broken, no way back; search engines may index empty pages                |
| Fix  | Return 404 with _"This product is no longer available"_ and a link to Products |

### F7 · Fonts don't load · P3

|      |                                                                                                       |
| ---- | ----------------------------------------------------------------------------------------------------- |
| Seen | `main.css` loads Google Fonts over `http://` → blocked → default font; 3 console errors on every page |
| Why  | Site doesn't look as designed; console noise hides real errors                                        |
| Fix  | Change `http://` to `https://` in `main.css` lines 5–7                                                |

## Usability concerns

### F8 · Mobile cart hides totals and remove button · P2

|      |                                                                                                                   |
| ---- | ----------------------------------------------------------------------------------------------------------------- |
| Goal | Remove an item on a phone                                                                                         |
| Seen | At 375px the Total column and × are off-screen until you swipe the table (`evidence/mobile/iphone-se-cart-*.png`) |
| Why  | Removing an item is a core task; customers may not find it                                                        |
| Fix  | On small screens show each item as a card: _"Rs. 500 × 1 = Rs. 500"_ + a visible **Remove** button                |

### F9 – F11 · Smaller usability points · P3

| #   | Seen                                                                    | Fix                                              |
| --- | ----------------------------------------------------------------------- | ------------------------------------------------ |
| F9  | 2 of 14 "top" results are shirts (matched by category); no result count | Show _"14 results for 'top'"_; document the rule |
| F10 | Search box label is only the placeholder, which disappears when typing  | Add a hidden `<label for="search_product">`      |
| F11 | 999 accepted (Rs. 499,500); no limit documented, so not a defect        | Cap at stock: _"Only 25 available"_              |

## Design preferences

| #   | Seen                                                                 | Fix                             |
| --- | -------------------------------------------------------------------- | ------------------------------- |
| F12 | "Tshirt" / "T-Shirt" / "T SHIRT"; one name in capitals; mixed dashes | Agree one naming style (IMP-06) |
| F13 | Footer says "Copyright © 2021"                                      | Show the current year (IMP-08)  |

## What works well

| Area            | Result                                                     | Tests                 |
| --------------- | ---------------------------------------------------------- | --------------------- |
| Search          | Correct results; page count matches API (14)               | TR-01, TR-19, CON-02  |
| Product details | Name, price, brand match everywhere for all 34 products    | TR-03, CON-01, CAT-01 |
| Images          | All 34 load                                                | CAT-02                |
| Add to cart     | Valid quantities add; clear confirmation                   | TR-04, TR-05, FE-05   |
| Cart maths      | Always correct (one item, two items, after removal)        | TR-06 to TR-08, FE-06 |
| Remove item     | Works on desktop and mobile; empty cart says so            | TR-08, TR-09, TR-28   |
| Checkout        | Login prompt keeps the cart; review shows correct total    | TR-14 to TR-16        |
| Mobile          | Whole journey works at 375px (page never scrolls sideways) | TR-22 to TR-25        |
| API             | Every response body matches the docs                       | API-A1 to API-A6      |
