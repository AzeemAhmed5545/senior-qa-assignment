# Technical Assessment (§2)

The journey from the brief, checked in depth: **search "top" → open product → choose quantity → add
to cart → check item and total.** Chrome 156 · 1440×900 and 375×667 · 29–30 Oct.

## 1. Journey

| Step             | Result                          | Evidence (`evidence/desktop/`)  |
| ---------------- | ------------------------------- | ------------------------------- |
| Search "top"     | 14 results (same as API)        | `01-search-top-1440.png`        |
| Open Blue Top    | Name, price, brand, stock shown | `03-pdp-qty2-1440.png`          |
| Quantity 2 → Add | "Added!" with View Cart         | `04-add-to-cart-modal-1440.png` |
| Cart             | Rs. 500 × 2 = **Rs. 1000** ✅   | `05-cart-qty2-1440.png`         |

**The journey works.** The problems are around it: quantity rules, control names, feedback.

## 2. API (summary)

Full details: [`API_CHECKS.md`](API_CHECKS.md)

| Request           | HTTP    | Body code | Result                                              |
| ----------------- | ------- | --------- | --------------------------------------------------- |
| Search `top`      | 200     | 200       | ✅ 14 products                                      |
| No match          | 200     | 200       | ✅ empty list                                       |
| Parameter missing | **200** | **400**   | Body matches docs; HTTP status **unclear** (AMB-01) |

No confirmed API defects.

## 3. Name and price in four places — Blue Top

| Source        | Name     | Price                  | Evidence                  |
| ------------- | -------- | ---------------------- | ------------------------- |
| API           | Blue Top | Rs. 500                | `evidence/api/A1-raw.txt` |
| Search result | Blue Top | Rs. 500                | `01-search-top-1440.png`  |
| Product page  | Blue Top | Rs. 500                | `03-pdp-qty2-1440.png`    |
| Cart (qty 2)  | Blue Top | Rs. 500 → **Rs. 1000** | `05-cart-qty2-1440.png`   |

✅ All agree. The catalogue audit confirms the same for all 34 products.

## 4. Frontend controls

**Markup inspected:**

```html
<input type="text" id="search_product" placeholder="Search Product" />
<button type="button" id="submit_search"><i class="fa fa-search"></i></button>
<label>Quantity:</label> <input type="number" id="quantity" value="1" min="1" />
<button type="button" class="btn btn-default cart">Add to cart</button>
```

| Control       | Check           | Result                                                  | Ref    |
| ------------- | --------------- | ------------------------------------------------------- | ------ |
| Search box    | Name            | Placeholder only                                        | IMP-07 |
| Search button | Name            | ❌ Empty (`button ""`)                                  | DEF-02 |
| Search        | Keyboard        | ❌ Enter does nothing (no `<form>`); Tab + Space works  | DEF-07 |
| Search button | Focus visible   | ❌ 1.19:1 change only (field is fine)                   | DEF-08 |
| Search        | Feedback        | ❌ No message when nothing is found                     | DEF-04 |
| Quantity      | Name            | ❌ Label not linked; unnamed field                      | DEF-03 |
| Quantity      | Input rules     | ❌ 0 and −1 added (`min="1"` not enforced)              | DEF-01 |
| Add to cart   | Name / keyboard | ✅ "Add to cart"; Tab + Enter works                     | —      |
| Add to cart   | Feedback        | ✅ for valid quantities · ❌ says "Added!" for 0 and −1 | DEF-01 |
| All           | Mobile 375px    | ✅ works · ⚠️ cart totals hidden until swipe            | IMP-09 |
| All           | Console         | ❌ 3 mixed-content errors; fonts never load             | DEF-11 |

Accessibility evidence: `evidence/technical/a11y-tree-*.yml`, `focus-1-search-field-tab.png`,
`focus-2-search-button-tab.png`

## 5. Conclusion — causes

| Defect    | Cause (seen from outside)                                       | Needs internal access      |
| --------- | --------------------------------------------------------------- | -------------------------- |
| DEF-01    | `cart.js` sends quantity unchecked; server accepts `quantity=0` | Server validation; payment |
| DEF-02/03 | Icon-only button; label without `for`                           | —                          |
| DEF-04    | No empty-result message (inferred from output)                  | Template code              |
| DEF-07    | Click-only handler, no `<form>`                                 | —                          |
| DEF-08    | `outline: none`; faint Bootstrap focus style                    | —                          |
| DEF-10    | Unknown IDs render an empty template with 200                   | Routing code               |
| DEF-11    | `main.css` imports fonts over `http://`                         | —                          |
| AMB-01    | API always returns HTTP 200, error code in body                 | Was it intended?           |

**Limits:** Chrome only · no screen reader · stopped before payment · no load or security testing.
