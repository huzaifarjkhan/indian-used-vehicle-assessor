# Indian Used-Vehicle Assessor — Reusable Assessment Skill

A portable, user-provided ChatGPT skill and standalone checklist. The skill is **not automatically installed** or given permanent access to future chats. To reuse: choose **Code > Download ZIP** on this repository, or download `SKILL.md`, then attach the file to a new conversation. You can also install the files in a compatible skill system.

## Quick start for future ChatGPT chats

> Use the Indian Used-Vehicle Assessor skill I attached. I am evaluating this car: [photos / listing / RC / VIN]. Extract all identifiers, verify online records you can access, explain any OTP/CAPTCHA blocks, investigate previous sale/accident/fraud records and prices if asked, then produce a complete objective HTML investigation report with copy-ready portal fields, linked sources, photo evidence and an interactive 134-point inspection checklist. Prioritize newly discovered discrepancies at the top. Do not assume a clean vehicle from no matches. Do not ask me again for data already in the attached documents.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Main AI operational instructions and decision rules |
| `references/portals-india.md` | Official website links, exact input fields, blocked access and results interpretation |
| `references/photo-document-protocol.md` | Photos and records to request and how to interpret them |
| `references/inspection-master.md` | Full 134-point annotated checklist |
| `references/pricing-and-transaction.md` | Comparable pricing, finance, ownership and handover |
| `templates/vehicle-data.json` | Vehicle JSON: blank until populated from evidence |
| `templates/checks.json` | Structured checklist sections and detailed descriptions |
| `templates/assessment-report.md` | Neutral report skeleton |
| `scripts/build_checklist.py` | Generates A4, locally markable HTML; standard Python 3, no dependencies |
| `output/Reusable_Used_Vehicle_Checklist.html` | Ready-to-use blank interactive/printable HTML |
| `examples/anonymized-case.md` | Example source interpretation without personal identifiers |

## Open the checklist

Download [`output/Reusable_Used_Vehicle_Checklist.html`](output/Reusable_Used_Vehicle_Checklist.html) and open it locally in Chrome or another modern browser. The checklist supports markable inspection items, progress export/import and A4 printing.

## Generate a new vehicle HTML checklist

1. Copy `templates/vehicle-data.json` to `vehicle.json`.
2. Populate the file only with documentary/photo facts. Leave unknowns blank. Use `recorded_flags` for official/supplied concerns: `{ "label":"Renewal pending", "detail":"Online fee paid but not inwarded", "source":"VAHAN screenshot", "checked_at":"YYYY-MM-DD" }`.
3. From this folder run:

```bash
python3 scripts/build_checklist.py --data vehicle.json --output vehicle_checklist.html
```

4. Open HTML in Chrome/Edge/Firefox. Change statuses and notes, use Export progress (JSON) or Import progress; optionally Print > Save as PDF, paper A4, scale 100% or fit.
5. If you upload the progress JSON in a future conversation, it can be used as part of the next iteration. Browser local storage persists only according to that browser's file URL and settings.

For a blank generic HTML checklist:

```bash
python3 scripts/build_checklist.py --data templates/vehicle-data.json --output output/Reusable_Used_Vehicle_Checklist.html
```

## Verification principles

- Screenshots and uploaded PDFs are evidence **of what the portal/document reported**, not universal certifications.
- Keep each result verbatim, dated and matched to VIN/registration. No data found is different from no accident.
- Official sources can require own login, registered-owner OTP or CAPTCHA. The skill never bypasses these; it guides the user.
- The user may request neutral reports only; no price or buying opinion without express request.
- Validate that generated files open in browsers before sharing. If interactive PDF causes problems, HTML is the stable primary output.

**Last portal research:** 3 Nov 2026. Recheck links/rules when assessing a new vehicle.

## Public-repository privacy

This repository contains reusable instructions, blank templates, and anonymized examples only. **Do not commit actual vehicle registration numbers, VINs, owner names, contact information, insurance policy numbers, RC scans, inspection reports, OTPs, or other buyer/seller records.** Keep completed assessments offline or in private repositories.

## Detailed HTML investigation report (new)

The repository now has **two** separate generators: `scripts/build_checklist.py` creates a standalone interactive checklist; `scripts/build_investigation_report.py` builds a richer, self-contained investigation report based on the Hyundai Getz report format, but using only anonymized reusable templates. See `references/html-investigation-report.md`.

Run the anonymized demo:

```bash
python3 scripts/build_investigation_report.py \\
  --data examples/anonymized-investigation-report.json \\
  --output output/Demo_Investigation_Report.html
```

For a new vehicle, make a **private copy** of `templates/investigation-report-data.json`, fill the IDs, official lookup results, photo observations, portal statuses, comparables (only if requested), and evidence ledger; then run the generator. It automatically derives VIN last-five/last-four and engine last-four characters and inserts them into `templates/portal-checks.json` website instructions. Use `--embed-images` for local photos; sensitive/identity images are excluded unless explicitly permitted in a **private** output. Never upload actual RC photos, owners' personal data, or live case JSON into the public GitHub repository.

The report includes red attention points first, 13 source links, copy buttons, a self-contained photo gallery, a 134-item interactive inspection checklist, progress import/export, and A4 browser printing. A static anonymized example appears in `output/Demo_Investigation_Report.html`.
