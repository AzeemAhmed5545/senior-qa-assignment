# Improvements (§5)

Suggestions, **not defects** — nothing here breaks a rule, so each needs an owner to decide. Defects
are in [`defects/DEFECTS.md`](../defects/DEFECTS.md).

**Priority:** P2 soon · P3 backlog · P4 nice to have

## Summary

| ID     | Suggestion                                          | Type       | Priority |
| ------ | --------------------------------------------------- | ---------- | -------- |
| IMP-09 | Mobile cart: show totals and Remove without swiping | Usability  | P2       |
| IMP-02 | Product name as the page's `<h1>`                   | Usability  | P2       |
| IMP-04 | API: real error status and JSON content type        | API        | P2       |
| IMP-01 | Maximum quantity linked to stock                    | Usability  | P3       |
| IMP-03 | Show result count; document what search matches     | Usability  | P3       |
| IMP-05 | Decide what a blank API search should do            | API        | P3       |
| IMP-06 | Consistent product names                            | Content    | P3       |
| IMP-07 | Label for the search box                            | Usability  | P3       |
| IMP-08 | Current year in the footer                          | Preference | P4       |

## Details

### IMP-09 · Mobile cart: show totals and Remove without swiping · P2

|            |                                                                                                         |
| ---------- | ------------------------------------------------------------------------------------------------------- |
| Seen       | At 375px the cart table is wider than the screen; Total and × are hidden until you swipe (TR-24, TR-28) |
| Why        | Removing an item is a core task; customers may not find it                                              |
| Suggestion | On small screens, one card per item: _"Rs. 500 × 1 = Rs. 500"_ + a visible **Remove** button            |
| Trade-off  | Needs responsive CSS and testing on several phones                                                      |

### IMP-02 · Product name as the page's `<h1>` · P2

|            |                                                                                              |
| ---------- | -------------------------------------------------------------------------------------------- |
| Seen       | No `<h1>` on any of the 34 product pages; the name is an `<h2>` like "Category" and "Brands" |
| Why        | Screen-reader users can't find the main heading; weaker SEO                                  |
| Suggestion | Change `<h2>Blue Top</h2>` to `<h1>` in the template (same styling)                          |
| Trade-off  | None visible                                                                                 |

### IMP-04 · API: real error status and JSON content type · P2

|            |                                                                                                     |
| ---------- | --------------------------------------------------------------------------------------------------- |
| Seen       | Errors return HTTP 200 with the code only in the body; JSON is sent as `text/html` (AMB-01, OBS-01) |
| Why        | Clients and monitoring that read the HTTP status treat failures as success                          |
| Suggestion | Return `400` with `application/json` — **or** change the docs to say "always HTTP 200"              |
| Trade-off  | Changing the status may break clients that rely on it; changing the docs is zero-risk               |

### IMP-01 · Maximum quantity linked to stock · P3

|            |                                                                 |
| ---------- | --------------------------------------------------------------- |
| Seen       | 999 accepted (Rs. 499,500); no limit is documented (was DEF-09) |
| Suggestion | Cap at stock: typing 999 shows _"Only 25 available"_            |
| Trade-off  | Needs a business rule; too low a cap blocks bulk buyers         |

### IMP-03 · Show result count; document what search matches · P3

|            |                                                                                      |
| ---------- | ------------------------------------------------------------------------------------ |
| Seen       | 2 of 14 "top" results are shirts matched by category "Tops & Shirts"; no count shown |
| Suggestion | Show _"14 results for 'top'"_; decide name-only vs name + category                   |
| Trade-off  | Category matching is arguably helpful — a product decision                           |

### IMP-05 · Decide what a blank API search should do · P3

|            |                                                                        |
| ---------- | ---------------------------------------------------------------------- |
| Seen       | `search_product=` returns all 34 products; not in the docs             |
| Suggestion | Document "blank = all products", or reject it like a missing parameter |

### IMP-06 · Consistent product names · P3

|            |                                                                                                       |
| ---------- | ----------------------------------------------------------------------------------------------------- |
| Seen       | "Tshirt" (#2), "T-Shirt" (#28–30), "T SHIRT" (#43, all capitals); #22 "-Pink"; #24 long dash "–"      |
| Why        | Looks careless; a search for "t-shirt" may miss "Tshirt"                                              |
| Suggestion | One style, e.g. _Title Case, "T-Shirt", " - " before the colour_. The catalogue audit flags new cases |

### IMP-07 · Label for the search box · P3

|            |                                                                                 |
| ---------- | ------------------------------------------------------------------------------- |
| Seen       | Only the placeholder "Search Product", which disappears when typing             |
| Suggestion | Hidden `<label for="search_product">Search products</label>` (no visual change) |

### IMP-08 · Current year in the footer · P4

|            |                                       |
| ---------- | ------------------------------------- |
| Seen       | "Copyright © 2021" on every page     |
| Suggestion | Render the current year automatically |
