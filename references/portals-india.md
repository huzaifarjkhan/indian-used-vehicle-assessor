# India Used-Vehicle Portal Directory — verified links and lookup recipes

**Checked 2026-11-03.** Dynamic portal routes, login rules, exact labels and availability change. Open the parent official site if a deep link fails. Never fill a guessed value merely to make a form submit. **Read-only checks only** unless user explicitly authorizes a transaction. For every lookup, capture screenshot/PDF, query identifiers, timestamp, exact status wording, portal name, and caveat.

## 1 — Core government sources (all-India)

| ID | Portal | Official URL | Where to click / what to enter | Captures / limitations |
|---|---|---|---|---|
| P01 | VAHAN National Register | https://vahan.parivahan.gov.in/nrservices/ | `Know Your Vehicle Details` / Vehicle Search; full registration number; CAPTCHA/login as requested | Make/model, fuel, variant, class, registered owner mask, registration/fitness expiry, insurance, PUC, financier if shown. Access/fields vary. Owner count might not be shown. |
| P02 | VAHAN Citizen Services | https://vahan.parivahan.gov.in/vahanservice/ | Select state/RTO; `Status > Know Your Application Status`; select registration or application no; open `Show Details`. | Pending registration renewal, tax application, inspection, fee/dispatch status. **Payment success != RTO inwarding/approval.** Other menu options like blacklist/tax differ across RTOs. |
| P03 | National Transport Repository | https://services.parivahan.gov.in/ntr/ | `SERVICE > Know Vehicle/DL Details`; authenticate using your own credentials as allowed; vehicle number; `RC Search`. | Date, fuel, status, `Accident History` count, insurance, challans, PUC/HSRP. Aggregate accident entry may lack underlying FIR/cause. Direct deep-linked results may fail without session. |
| P04 | National e-Challan | https://echallan.parivahan.gov.in/ | `Check Challan Status` / `Vehicle Number` with registration number and, if prompted, first registration date and CAPTCHA | Zero results means none **in that portal's returned data**, not all state/local databases. Avoid payment unless owner approves. |
| P05 | National PUC | https://vahan.parivahan.gov.in/puc/views/PucCertificate.xhtml | Vehicle registration, last five chassis characters and CAPTCHA where required | PUC issuance/validity; an unavailable record may need physical certificate confirmation. |
| P06 | NCRB / Digital Police | https://digitalpolice.gov.in/DigitalPolice/ | `Central Citizen Services > Generate Vehicle NOC`; enter permitted own phone/name/OTP/CAPTCHA; search registration or VIN or engine no | Crime/stolen involvement database. A nationwide vehicle NOC is preferable to a partial regional no-match. Portal sometimes has OTP failure; do **not** circumvent. |
| P07 | NCRB Citizen login | https://www.digitalpolicecitizenservices.gov.in/centercitizen/login.htm | Log in with user's own phone, OTP, name and CAPTCHA if accessible; generate NOC. | Site may stall or not respond; record as `BLOCKED` and seek official assistance instead of trying unverified IPs. |
| P08 | RC renewal guidance | https://staging.parivahan.gov.in/parivahan/en/print/pdf/node/15 | Reference for **Form 25** and application requirements (not a vehicle lookup). | Private/non-transport RC renewal; verify current local requirements. |
| P09 | Transfer of ownership | https://mparivahan.parivahan.gov.in/mstatic/english/rc-info-ownership.html | Reference for **Forms 29 and 30** for normal sale; see seller/buyer process in actual VAHAN service. | NOC for interstate/other circumstances; don't assume every local transfer needs an interstate NOC. |
| P10 | Hypothecation termination | https://mparivahan.parivahan.gov.in/mstatic/english/rc-info-hp-termination.html | If finance record is shown, verify lender due clearance and Form 35 where applicable | Form 35 relates to terminating finance; it is not generic proof of free title if financier still recorded. |
| P11 | VAHAN public user manuals | https://staging.parivahan.gov.in/vahaneservice/usermanual/ | Steps/screens for services and field expectations. | Some pages describe newer workflows or state-specific migration. |

## 2 — Maharashtra-specific routes

| ID | Portal | URL | Inputs / action | Key limitation |
|---|---|---|---|---|
| P12 | Maharashtra Traffic e-Challan | https://mahatrafficechallan.gov.in/payechallan/PaymentService.htm | Vehicle number; **last 4 characters** of chassis **or** engine number; Submit | May OTP the existing RC-registered mobile to view/associate records. Cannot use buyer's number without linked-owner confirmation. Helpdesk 8448448960 per official website. |
| P13 | Maharashtra Transport HSRP | https://transport.maharashtra.gov.in/1125/HSRP | `HSRP online booking` > RTO selection or official vendor. Registration, last 5 chassis/engine and owner/fitment details may be needed. | Government service page warns of unofficial/fraudulent booking links; use only linked vendors. Applicable requirements depend on vehicle registration date. |
| P14 | Maharashtra HSRP apply | https://transport.maharashtra.gov.in/1222/Apply-High-Security-Registration-Plate-Online | Choose registering RTO, then follow authorized provider | Do not invent status if user cannot complete booking. |
| P15 | Maharashtra tax/RTO procedures | https://transport.maharashtra.gov.in/1185/RTO-Procedure | Relevant forms and state process reference; VAHAN transaction statuses are vehicle-specific. | Fees/taxes/rates must be rechecked at time of inspection. |
| P16 | Mumbai Police stolen/unclaimed | https://mumbaipolice.gov.in/stolen_vehicles | Registration or chassis or engine, CAPTCHA, Submit | In a 2026 example the form reloaded blank despite successful GET request; this is **inconclusive**, not zero. If page malformed, record as blocked. |

## 3 — Regional police, manufacturer and records

| ID | Portal | URL | Inputs / action | Notes |
|---|---|---|---|---|
| P17 | ZIPNET stolen vehicle | https://zipnet.delhipolice.gov.in/VehiclesMobiles/MissingVehicles | Open `Search`, fill registration, run; separately reset and fill VIN; save results. | Participating states largely northern India; **not** nationwide clearance. Do not confuse the on-page `Add`/`Edit` sections with searching. |
| P18 | ZIPNET unclaimed/seized | https://zipnet.delhipolice.gov.in/vehiclesmobiles/unclaimedseizedvehicles/ | Search plate/VIN, if relevant; record exact hit or no hit | Regional, incomplete nationally. |
| P19 | Maruti Suzuki campaigns | https://www.marutisuzuki.com/important-information-for-customers | Full VIN/Chassis (usually 17 chars beginning MA3/MBH/MBJ), click `Check Now`. | Result `does not need attention under any campaign` means no open campaign indicated by checker, **not** full service or accident record. |
| P20 | Maruti authorized service | https://www.marutisuzuki.com/ | Manufacturer service booking/contact; ask vehicle owner to authorize service/body-shop history lookup by VIN. | Private service data may not be publicly viewable. Authorised workshop independently chosen is preferable. |
| P21 | NTR data sharing context | https://parivahan.gov.in/sites/default/files/policy/data-sharing-policy.pdf | Background, provenance/data-access limitations of National Transport Repository. | **Don't assume** NTR accident count gives severity unless a real linked record is displayed. |

## 4 — Field cookbook, in order

1. **Plate**: Normalize `MH 01 AB 1234` => `MH01AB1234`; keep formatted original too. VIN must be from authoritative physical stamp/doc, not a guessed plate lookup.
2. **VIN/Chassis**: Copy full alphanumeric exactly; derive `last4 = VIN[-4:]` and `last5 = VIN[-5:]` **only** after confirming entire VIN. Case-insensitive entry usually works but prefer uppercase; don't omit a character.
3. **Registration date**: Use RC `Date of Registration` / `First Regn` in website's requested format (DD-MM-YYYY or date picker), not seller-ad manufacture year.
4. **Engine number**: Record full engine number from physically stamped engine / RC; **never fabricate** from VIN.
5. **RTO application**: Distinguish `Renewal Application No`, `MV Tax Application No`, receipt number, payment transaction number, bank reference, GRN and insurer policy; they are not interchangeable.
6. **RC validity**: Check registration/fitness valid-until on actual VAHAN RC details, and re-check **application status** separately. A paid pending renewal may remain legally unresolved.
7. **Owner count**: Record only if a reliable RC/VAHAN/ownership transfer history explicitly supplies it. Masked owner name alone does not prove first owner.
8. **Owner OTP**: If sent to registered mobile, **owner must participate**. Don't attempt unapproved relinking.
9. **NCRB**: If OTP/CAPTCHA never arrives, state `BLOCKED – portal service unavailable` and request dealer/seller's official NOC or official police assistance; keep regional searches as limited supplementary evidence.
10. **Manufacturer recall**: Enter actual VIN, note exact result string and date. Re-check on a future purchase date because campaigns can change.

## 5 — Status interpretation examples

| Raw UI message | Evidence statement | What NOT to conclude |
|---|---|---|
| `ONLINE TRANSACTION SUCCESS ... BUT NOT INWARDED` | Online fee accepted; no RTO inwarding recorded in that application response. | Inspection passed, RC renewed or application rejected. |
| `TRANSACTION COMPLETE` under MV Tax | This specific tax payment transaction completed. | All future periods tax-paid or RC valid. |
| `RC DISPATCH: NO RECORDS FOUND` | No dispatch record surfaced in the lookup. | RC not approved **solely** on this field. |
| `Fitness/REGN: <past date>` for private vehicle | Displayed legal registration/fitness-related expiry has passed. | Specific repair cause or automatic permission to drive. |
| `Accident History: 1` | Portal reports one record/indicator, details not shown. | Serious crash, total loss, airbag deployment or minor scrape. |
| `No challan found` (national) | No record returned by national e-Challan for searched identifiers. | Maharashtra/state police have zero outstanding fines. |
| `No data available in ZIPNET table` | No accessible regional record matched that query. | All-India stolen/court/accident clearance. |
| `No recall campaign attention` | Manufacturer campaign checker shows no attention required at that moment. | Entire car mechanically sound or accident-free. |

## 6 — Evidence capture & access

For each result save a screenshot or PDF along with portal URL, checked local date, raw query string, title, search method, visible status, and `blocked_by` if applicable (`captcha`, `owner_otp`, `site_error`, `login`, `paywall`). If a source is official but the export is unsigned, cite its official generating URL/screenshot rather than dismissing it based on PDF generator metadata alone. If a page is in a user's authenticated session, don't claim the same record can be replayed by opening their deep link without that session.