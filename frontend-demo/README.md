# Frontend Fix — Quantity Field (§3)

Fixes **DEF-01** (0 and −1 accepted) and **DEF-03** (field has no name). Chrome 156 · 30 Oct.

## Before → After

|                    | Before                       | After                                       |
| ------------------ | ---------------------------- | ------------------------------------------- |
| Quantity `0`       | Sent to cart, "Added!" shown | Blocked: _"Enter a quantity of 1 or more."_ |
| Quantity `2`       | Added                        | Added (unchanged)                           |
| Screen-reader name | None                         | "Quantity:"                                 |

## Why this change

It's on the brief's main journey and fixes the only problem that affects money (cart can show **Rs.
−500**).

## Cause

The site's `cart.js` sends the typed value straight to the server, which accepts it. `min="1"` does
nothing because the field isn't in a `<form>`. The `<label>` has no `for`.

## The change — `improvement.js`

1. Links the label to the field (`for="quantity"`).
2. Before adding to cart, allows only whole numbers ≥ 1. Otherwise: no request, red message, field
   marked invalid, focus returned.
3. Valid quantities go through unchanged.

Works on any product page; does nothing on other pages.

**In the real code:** add the same check in `cart.js`, add `for="quantity"` to the label, and
**validate on the server** too.

## Trade-offs

- Frontend only — a direct `/add_to_cart/1?quantity=-1` still works until the server is fixed.
- No maximum (stock rule unknown).
- `1.5` and `1e2` are rejected (safer).

## Verification

| #   | Check                             | Result                                |
| --- | --------------------------------- | ------------------------------------- |
| 1   | Before: qty 0                     | Request sent, "Added!" (defect shown) |
| 2   | After: qty 0                      | ✅ Blocked with message               |
| 3   | After: −1, blank, 1.5, 1e2, space | ✅ All blocked, 0 requests            |
| 4   | Field name                        | ✅ "Quantity:"                        |
| 5   | Qty 2 using keyboard only         | ✅ Added as before                    |
| 6   | Cart total                        | ✅ Rs. 1000, one row                  |
| 7   | Product 2 at 375px                | ✅ Blocked, fits screen               |
| 8   | Page that isn't a product page    | ✅ No change                          |

Not tested: real screen reader, other browsers.

## Evidence (`evidence/`)

`01-before-qty0-added-modal.png` · `02-after-qty0-blocked.png` · `03-after-qty2-added.png` ·
`04-after-cart-qty2-total-1000.png` · `05-after-mobile-375-product2-blocked.png` ·
`06-local-demo-after.png`

## Try it

**Live site:** open a product page → F12 → Console → paste `improvement.js` → type `0` → Add to
cart.

**Local:** `python -m http.server 8765` in this folder → open
`http://127.0.0.1:8765/local-demo.html` → click **Apply improvement**.
