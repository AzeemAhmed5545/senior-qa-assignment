"""
Self-check for catalogue_audit.py - proves that problems are reported, not hidden.

Runs the real audit against the live site but injects three faults:
  product 5  - product page request times out  -> must appear under "Checks not completed"
  product 6  - product page shows a different price -> must be flagged "price differs"
  product 7  - main image returns 404           -> must be flagged "main image not loading"

Output goes to a temporary folder; the real reports in catalogue/reports are not touched.

Usage (from the repository root):
    python scripts/catalogue_audit_selfcheck.py
"""

import csv
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalogue_audit as audit  # noqa: E402

audit.OUT_DIR = Path(tempfile.mkdtemp(prefix="catalogue_selfcheck_"))
audit.RETRIES = 0
real_fetch = audit.fetch


def faulty_fetch(url, data=None):
    if url.endswith("/product_details/5"):
        return None, "", "", "TimeoutError: injected by self-check"
    if url.endswith("/get_product_picture/7"):
        return 404, "text/html", "", ""
    status, ctype, text, err = real_fetch(url, data)
    if url.endswith("/product_details/6"):
        text = text.replace("<span>Rs. 400</span>", "<span>Rs. 450</span>")
    return status, ctype, text, err


audit.fetch = faulty_fetch
audit.main()

rows = {r["product_id"]: r for r in csv.DictReader(open(audit.OUT_DIR / "latest.csv", encoding="utf-8-sig"))}
checks = [
    ("Product 5 timeout is listed as not completed", "request failed" in rows["5"]["checks_not_completed"]),
    ("Product 5 is not reported as a pass", rows["5"]["name_match"] == "not checked"),
    ("Product 6 price difference is flagged", rows["6"]["price_match"] == "N" and "price differs" in rows["6"]["facts_failed"]),
    ("Product 7 broken image is flagged", rows["7"]["main_image_ok"] == "N" and "main image not loading" in rows["7"]["facts_failed"]),
    ("Untouched product 1 still passes name and price", rows["1"]["name_match"] == "Y" and rows["1"]["price_match"] == "Y"),
]
print("\nSelf-check results:")
for label, ok in checks:
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
print(f"(test report written to {audit.OUT_DIR})")
sys.exit(0 if all(ok for _, ok in checks) else 1)
