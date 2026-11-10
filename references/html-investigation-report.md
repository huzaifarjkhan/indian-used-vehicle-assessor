# Detailed HTML Investigation Report — Reusable Workflow

The new report generator follows the structure of the earlier Hyundai Getz assessment, **without publishing any real Getz RC, VIN, registration or owner's identifying information**. It is separate from the generic 134-point inspection checklist.

## When to use

For requests to investigate a second-hand car from photos, registration, RC, invoices or listing, complete all accessible read-only checks first. Create a **private copy** of `templates/investigation-report-data.json`; fill only source-backed facts. Add `report_date`, `records`, `observations`, `evidence` and `attention_points`, and mark unknown fields empty.

## Required report sections in order

1. **Attention points / red flags first**, grouped by documented status versus visual concern versus unverified. Quote exact status messages and their dates.
2. **Key metrics**: owner serial, first registration, printed RC validity versus current VAHAN validity.
3. **Copyable identifiers**: full registration, VIN, engine, automatically derived last 5/4 VIN and engine last 4, RTO, RC/PUC/insurance/tax validity, application/payment refs. Do not infer missing identifiers.
4. **Portal-by-portal records**: exact results, source, checked date, coverage and limitations. Distinguish no match from cleared; paid fee from approved RC; manufacturer no recall from roadworthy.
5. **Photo findings**: visible physical condition and plausible follow-up tests. Never claim structural/airbag/flood damage from an exterior photo alone.
6. **Official lookup guide cards**: clickable official link, navigation path, and exact values copied from the canonical IDs. Cover VAHAN, NTR, state/national challan, PUC, NCRB, ZIPNET, Mumbai Police, recalls, OEM service and HSRP as relevant. Confirm URLs and login requirements at use time.
7. **Missing evidence**: physical VIN and engine stamp, prior owner and finance/HP status, claim/service/bodyshop history, odometer and cold-start video, independent lift and mechanical inspection.
8. **Comparable listings** only when the user asks for pricing: same region/year/variant/fuel, dated direct links, asking price is not completed sale price.
9. **Photo evidence gallery**: embed only photos approved for private reporting. RC/identity images with owner addresses or numbers excluded by default.
10. **134-point interactive checklist**, with statuses, notes, export/import JSON, local browser progress, and A4 print.
11. **Evidence ledger and inspection sign-off**, including uncertainty.

## Commands

```bash
python3 scripts/build_investigation_report.py \
  --data examples/anonymized-investigation-report.json \
  --output output/Demo_Investigation_Report.html
```

To embed photos from the same local folder as the case data:

```bash
python3 scripts/build_investigation_report.py --data /private/vehicle-investigation.json \
  --output /private/vehicle-report.html --embed-images
```

The extra flag `--include-sensitive-images` should only be used with the user's authorization for a **private** copy. Never publish filled reports, real VINs/plates, RC photos, addresses, insurance policy numbers or OTPs on this public repository.

## Data-entry conventions

- `attention_points`: `{ "title":"...", "detail":"...", "evidence":"Source + date" }`
- `records`: `{ "status":"Recorded|Checked|Unverified|Blocked|Conflicting", "subject":"...", "result":"exact portal text", "source":"portal name", "checked_at":"YYYY-MM-DD" }`
- `observations`: `{ "area":"...", "observation":"...", "limitations":"...", "follow_up":"...", "evidence":"P03" }`
- `portals`: override any `id` from `templates/portal-checks.json` with a result `status` or `skip:true` for irrelevant brands.
- `photos`: `{ "id":"P01", "path":"photos/front.jpg", "caption":"Front three-quarter", "observation":"...", "sensitive":false }`.
- `evidence`: `{ "id":"E01", "source":"RC card", "result":"...", "date":"YYYY-MM-DD", "limitation":"Photographed document; current status unverified" }`.

## Quality checks

Test the HTML in a browser: red section first; every known ID copies correctly; 134 check statuses; import/export JSON; the links and date/coverage labels; opt-in photo embedding and sensitive default omission; A4 print via Ctrl+P. Browser/localStorage behavior can differ for file:// URLs. Record technical blocks as inconclusive; never bypass CAPTCHA/OTP.
