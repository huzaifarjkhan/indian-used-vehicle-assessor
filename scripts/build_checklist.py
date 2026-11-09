#!/usr/bin/env python3
"""Offline, dependency-free India used-car inspection HTML generator.

Usage:
  python3 scripts/build_checklist.py --data templates/vehicle-data.json --output output/Reusable_Used_Vehicle_Checklist.html

The output includes no external JS, tracking, fonts or CSS. Statuses/notes can be
marked in-browser and exported to JSON for carrying forward to another session.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from collections import OrderedDict
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
E = lambda s: html.escape(str(s) if s is not None else "", quote=True)

PORTALS = [
    ("VAHAN — vehicle RC details", "https://vahan.parivahan.gov.in/nrservices/", "Registration number; login/CAPTCHA may apply", "P01"),
    ("VAHAN — citizen services", "https://vahan.parivahan.gov.in/vahanservice/", "Status > Know Your Application Status; registration or application number", "P02"),
    ("National Transport Repository", "https://services.parivahan.gov.in/ntr/", "SERVICE > Know Vehicle/DL Details; RC Search; login/OTP if prompted", "P03"),
    ("National e-Challan", "https://echallan.parivahan.gov.in/", "Vehicle no; registration date and CAPTCHA if requested", "P04"),
    ("PUC certificate", "https://vahan.parivahan.gov.in/puc/views/PucCertificate.xhtml", "Vehicle registration; last 5 VIN characters; CAPTCHA if requested", "P05"),
    ("NCRB — Digital Police", "https://digitalpolice.gov.in/DigitalPolice/", "Central Citizen Services > Generate Vehicle NOC; own login and OTP", "P06"),
    ("Maharashtra e-Challan", "https://mahatrafficechallan.gov.in/payechallan/PaymentService.htm", "Registration; last 4 VIN/engine characters; may need RC-owner OTP", "P12"),
    ("Maharashtra HSRP", "https://transport.maharashtra.gov.in/1125/HSRP", "Registration and selected RTO; fitment/booking with official provider", "P13"),
    ("Mumbai Police — stolen/unclaimed", "https://mumbaipolice.gov.in/stolen_vehicles", "Registration OR chassis/engine; CAPTCHA; may not display status", "P16"),
    ("ZIPNET — regional stolen vehicles", "https://zipnet.delhipolice.gov.in/VehiclesMobiles/MissingVehicles", "Search registration and VIN separately; regional records only", "P17"),
    ("Maruti Suzuki VIN recalls", "https://www.marutisuzuki.com/important-information-for-customers", "Full VIN; Check Now. Manufacturer-specific, use other OEM for other makes", "P19"),
    ("Official ownership transfer guidance", "https://mparivahan.parivahan.gov.in/mstatic/english/rc-info-ownership.html", "Form 29/30 guidance, not a vehicle-specific search", "P09"),
    ("Form 35 / finance closure guidance", "https://mparivahan.parivahan.gov.in/mstatic/english/rc-info-hp-termination.html", "Only where a bank/hypothecation entry exists", "P10"),
]

FIELDS = [
    ("registration", "Registration number"), ("formatted_registration", "Plate as photographed"),
    ("vin", "Full chassis / VIN"), ("engine_number", "Engine number (full)"),
    ("make", "Manufacturer"), ("model", "Model"), ("variant", "Variant / trim"),
    ("fuel", "Fuel"), ("transmission", "Transmission"), ("vehicle_class", "Vehicle class"),
    ("first_registration", "First registration date"), ("manufacture_month_year", "Manufacture month/year"),
    ("rto", "RTO authority"), ("odometer", "Odometer in photo / test"),
    ("owner_count", "Registered owner count"), ("registration_valid_to", "Registration valid through"),
    ("mv_tax_valid_to", "MV tax valid through"), ("puc_valid_to", "PUC valid through"),
    ("insurance_company", "Insurance company"), ("insurance_policy_number", "Policy number"),
    ("insurance_valid_to", "Insurance valid through"), ("renewal_application", "Renewal application number"),
    ("tax_application", "MV tax application number"), ("receipt_number", "RTO receipt number"),
    ("grn", "GRN / payment reference"), ("loan_or_hypothecation", "Loan / financier (if shown)"),
]

STYLE = r"""
:root{--ink:#172b3c;--sub:#5b6878;--teal:#006e80;--red:#a42d34;--redbg:#fff1f1;--border:#d5dee6;--paper:#fff;--bg:#eef3f7;--mint:#edfaf6}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);font:14px/1.5 system-ui,-apple-system,Segoe UI,Arial,sans-serif;color:var(--ink)}
a{color:#006a84;text-decoration:underline;text-underline-offset:2px;overflow-wrap:anywhere}input,select,textarea,button{font:inherit}button{cursor:pointer;border:1px solid var(--teal);background:var(--teal);color:white;border-radius:7px;padding:8px 13px}button.secondary{background:white;color:var(--teal)}
main{max-width:1040px;margin:22px auto 80px;background:white;box-shadow:0 12px 36px #163f5921}
.head{background:#142c40;color:#fff;padding:24px 35px 23px}.kicker{font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:#9bd6e0;font-weight:700}.head h1{font-size:23px;margin:9px 0 7px;line-height:1.2}.head p{font-size:12px;color:#d2e1ed;margin:0}.toolbar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:12px 35px;background:#e8f3f6;border-bottom:1px solid #d4e6ed;position:sticky;top:0;z-index:5}.toolbar small{color:#435969}.toolbar input[type=file]{max-width:200px}.content{padding:0 35px 36px}
.sec{margin-top:22px;padding-top:3px;break-inside:auto}.sec h2{margin:0 0 12px;color:#16384b;font-size:17px;letter-spacing:-.2px;border-bottom:2px solid #c5e0e7;padding:0 0 7px;break-after:avoid}.sec h2 small{font-size:11px;color:#657688;font-weight:400;margin-left:8px}.sec p.help{font-size:12px;color:var(--sub);margin:0 0 10px}.redSec{background:var(--redbg);border:1px solid #eac1c1;border-radius:8px;padding:16px 17px 10px;margin-top:17px}.redSec h2{color:#971b23;border-bottom-color:#e7afb5}
.summary{border:1px solid #e7b5b9;border-left:5px solid #ad2d37;background:#fff8f8;padding:10px 13px;margin:12px 0}.summary p{margin:0;color:#633a40;font-size:12px}.flag-row{padding:6px 0;border-bottom:1px solid #f3d9d9;font-size:12px}.flag-row strong{display:block}.flag-row span{color:#6f5960}
.ident{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px}.ident label{display:block;font-size:11px;color:#536779;font-weight:650;break-inside:avoid}.ident input{display:block;margin-top:4px;width:100%;min-height:31px;padding:5px 8px;border:1px solid var(--border);border-radius:5px;background:#fbfdff;font-size:12px;color:var(--ink)}.derived{display:flex;gap:14px;margin-top:10px;padding:9px;border-radius:6px;background:#f0f7f8;font:12px ui-monospace,Consolas,monospace}
.check{border-bottom:1px solid #e4ebf0;padding:8px 0 9px;display:grid;grid-template-columns:minmax(0,1fr) 142px;gap:6px 12px;break-inside:avoid}.check.critical{border-left:3px solid #d9a0a5;padding-left:9px}.check-left{display:flex;gap:10px;align-items:flex-start}.check-left input[type=checkbox]{accent-color:#00768a;transform:scale(1.05);margin-top:3px}.check b{font-size:12.2px;display:block}.check code{color:#75909b;font-size:9px;white-space:nowrap}.check p{font-size:11.3px;color:#526170;margin:2px 0 0}.check-status select{width:100%;padding:4px;border:1px solid var(--border);border-radius:4px;background:white;font-size:11px}.check-note{grid-column:1/-1;width:100%;padding:4px 7px;border:1px solid #e4ecf2;background:#fcfdff;border-radius:4px;font-size:11px;min-height:25px;resize:vertical}.check-note::placeholder{color:#9da9b2}
.link-table{border-collapse:collapse;width:100%;font-size:11px}.link-table th,.link-table td{text-align:left;border-bottom:1px solid #dde4ea;padding:7px 8px;vertical-align:top}.link-table th{background:#f0f5f7;color:#274355}.link-table tr{break-inside:avoid}.badge{display:inline-block;border-radius:999px;font-size:10px;background:#e8f6f5;color:#145f5a;padding:2px 7px}
.emphasis{font-weight:700;color:#a02f38}.note{font-size:11px;color:var(--sub);background:#f3f7fb;border-radius:5px;padding:8px 10px}.longnotes{width:100%;min-height:78px;border:1px solid var(--border);padding:9px;border-radius:5px;font:12px/1.5 system-ui;background:#fcfdff}.foot{text-align:center;color:var(--sub);font-size:10px;border-top:1px solid #d9e3eb;padding:16px}.smallmono{font:10.5px/1.45 ui-monospace,Consolas,monospace}
@media(max-width:700px){main{margin:0}.head{padding:18px}.toolbar{padding:11px 17px}.content{padding:0 15px 20px}.ident{grid-template-columns:repeat(2,minmax(0,1fr))}.check{grid-template-columns:minmax(0,1fr) 114px}.head h1{font-size:20px}}
@page{size:A4;margin:12mm 11mm}
@media print{html,body{background:#fff!important;-webkit-print-color-adjust:exact;print-color-adjust:exact;font-size:10px}main{max-width:none;margin:0;box-shadow:none}.head{padding:14px 17px}.head h1{font-size:17px}.toolbar,.no-print{display:none!important}.content{padding:0 14px 10px}.redSec{margin-top:12px}.sec{margin-top:16px}.sec h2{font-size:13.8px;margin-bottom:6px;padding-bottom:5px}.ident{gap:5px;grid-template-columns:repeat(3, minmax(0,1fr))}.ident input{min-height:22px;padding:2px 4px;font-size:9px}.ident label{font-size:8.7px}.check{padding:4px 0 5px;gap:2px 7px;grid-template-columns:minmax(0,1fr) 106px}.check-left{gap:5px}.check b{font-size:9px}.check p{font-size:8.6px}.check-note{font-size:8.5px;min-height:17px;padding:1px 4px}.check-status select{font-size:8.2px;padding:1px}.link-table th,.link-table td{font-size:8.3px;padding:5px}.foot{font-size:8px}.no-print{display:none!important}.note{font-size:9px}}
"""

SCRIPT = r"""
(function(){
'use strict';
const storageKey='used_vehicle_checklist:'+location.pathname;
const fields=()=>[...document.querySelectorAll('input[data-persist],textarea[data-persist],select[data-persist]')];
const snapshot=()=>{const v={};fields().forEach(e=>v[e.id]=e.type==='checkbox'?e.checked:e.value);return {format:'indian-used-vehicle-assessor-v1',savedAt:new Date().toISOString(),values:v};};
const update=()=>{
  let verified=0, issue=0, blocked=0, count=0;
  document.querySelectorAll('select[data-check]').forEach(e=>{count++;if(e.value==='verified')verified++;if(e.value==='issue')issue++;if(e.value==='blocked')blocked++;
    const cb=document.getElementById(e.dataset.check+'_done');if(cb)cb.checked=e.value==='verified';});
  document.getElementById('progress').textContent=verified+' verified · '+issue+' issues · '+blocked+' blocked · '+count+' total';
  const vin=(document.getElementById('id_vin')?.value||'').trim().toUpperCase();
  document.getElementById('last4').textContent=vin.length>=4?vin.slice(-4):'Not available';
  document.getElementById('last5').textContent=vin.length>=5?vin.slice(-5):'Not available';
};
const save=()=>{try{localStorage.setItem(storageKey,JSON.stringify(snapshot()));}catch(err){} update();};
const apply=(data)=>{if(!data||!data.values)return;fields().forEach(e=>{if(Object.prototype.hasOwnProperty.call(data.values,e.id)){if(e.type==='checkbox')e.checked=!!data.values[e.id];else e.value=data.values[e.id]}});update();};
try{const s=localStorage.getItem(storageKey);if(s)apply(JSON.parse(s));}catch(err){}
fields().forEach(e=>e.addEventListener('change',()=>{if(e.matches('input[type=checkbox][data-check]')){const sel=document.getElementById(e.dataset.check+'_status');if(sel)sel.value=e.checked?'verified':'not_checked';}save();}));
fields().forEach(e=>e.addEventListener('input',save));
update();
document.getElementById('export').addEventListener('click',()=>{
  const data=JSON.stringify(snapshot(),null,2);const blob=new Blob([data],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='vehicle_checklist_progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),800);
});
document.getElementById('import').addEventListener('change',e=>{
  const f=e.target.files&&e.target.files[0];if(!f)return;const rd=new FileReader();rd.onload=()=>{try{const data=JSON.parse(rd.result);if(data.format!=='indian-used-vehicle-assessor-v1')throw new Error('Unexpected format');apply(data);save();alert('Progress imported');}catch(err){alert('Import failed: '+err.message)}};rd.readAsText(f);
});
document.getElementById('print').addEventListener('click',()=>window.print());
document.getElementById('clear').addEventListener('click',()=>{if(confirm('Clear saved checklist progress for this file?')){try{localStorage.removeItem(storageKey);}catch(err){} document.querySelectorAll('select[data-check]').forEach(s=>s.value='not_checked');document.querySelectorAll('[data-check][type=checkbox]').forEach(e=>e.checked=false);document.querySelectorAll('textarea[data-persist]').forEach(e=>e.value='');update();}});
})();
"""


def render(data: dict, checks: list[dict]) -> str:
    title=E(data.get('report_title') or 'Second-Hand Vehicle Verification and Inspection Checklist')
    ids=data.get('identifiers') or {}
    output=[]
    output.append('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><style>'+STYLE+'</style></head><body>')
    output.append('<main><header class="head"><div class="kicker">India · Evidence-first used vehicle assessment</div><h1>'+title+'</h1><p>Vehicle-specific verified facts, legal records, condition checks, and evidence notes. Not a fitness certificate or legal title warranty.</p></header>')
    output.append('<div class="toolbar no-print"><button id="print">Print / Save PDF</button><button id="export" class="secondary">Export progress (JSON)</button><label style="display:inline-block">Import progress <input id="import" type="file" accept="application/json" style="font-size:11px"></label><button id="clear" class="secondary">Clear statuses</button><small id="progress">Loading...</small></div><div class="content">')
    output.append('<section class="redSec" id="redflags"><h2>01 · Record flags and unresolved checks — review first</h2>')
    output.append('<p class="help">These flags are questions requiring documentary or physical verification. A blank section is not evidence that a car is clear.</p>')
    rec=data.get('recorded_flags') or []
    if rec:
        output.append('<div class="summary"><p><strong>Recorded findings from input sources:</strong></p>')
        for f in rec:
            output.append('<div class="flag-row"><strong>'+E(f.get('label',''))+'</strong><span>'+E(f.get('detail',''))+' · '+E(f.get('source','source not supplied'))+' · '+E(f.get('checked_at','date not supplied'))+'</span></div>')
        output.append('</div>')
    else:
        output.append('<div class="summary"><p>No vehicle-specific findings have been entered. Run the checks below before recording a conclusion.</p></div>')
    groups=OrderedDict()
    for item in checks: groups.setdefault(item['section'],[]).append(item)
    def render_checks(items):
        buf=[]
        for row in items:
            i=E(row['id']);desc=E(row.get('description',''));title2=E(row.get('title',''));applies=E(row.get('applicability','all'))
            suffix='' if applies=='all' else ' <span class="badge">'+applies+'</span>'
            status=E((data.get('inspection_item_status') or {}).get(row['id'],'not_checked'))
            buf.append('<article class="check '+('critical' if row.get('priority')=='critical' else '')+'">')
            buf.append('<div class="check-left"><input aria-label="Mark '+title2+' verified" type="checkbox" id="'+i+'_done" data-check="'+i+'" data-persist'+(' checked' if status=='verified' else '')+'><div><b><code>'+i+'</code> '+title2+suffix+'</b><p>'+desc+'</p></div></div>')
            buf.append('<div class="check-status"><select aria-label="Status of '+title2+'" id="'+i+'_status" data-check="'+i+'" data-persist>')
            for v,lab in [('not_checked','Not checked'),('verified','Verified / done'),('issue','Issue / discrepancy'),('blocked','Blocked / need owner'),('na','Not applicable')]:
                buf.append('<option value="'+v+'"'+(' selected' if status==v else '')+'>'+lab+'</option>')
            buf.append('</select></div><input class="check-note" type="text" data-persist id="'+i+'_notes" placeholder="Evidence / measurement / source / date / follow-up notes"></article>')
        return ''.join(buf)
    output.append(render_checks(groups.pop('RED-FLAG REVIEW — SCREEN FIRST',[])))
    output.append('</section>')
    output.append('<section class="sec" id="identifiers"><h2>02 · Vehicle identifiers and reference numbers</h2><p class="help">Enter exact values from photographs and authoritative documents. VIN suffixes update automatically. Unknown fields should remain blank.</p><div class="ident">')
    for key,label in FIELDS:
        output.append('<label for="id_'+E(key)+'">'+E(label)+'<input id="id_'+E(key)+'" data-persist value="'+E(ids.get(key,''))+'" placeholder="Not verified"></label>')
    output.append('</div><div class="derived"><span>VIN last 4: <strong id="last4">Not available</strong></span><span>VIN last 5: <strong id="last5">Not available</strong></span></div></section>')
    evidence=data.get('evidence') or []
    if evidence:
        output.append('<section class="sec"><h2>03 · Evidence ledger (user-provided)</h2><table class="link-table"><thead><tr><th>Record</th><th>Result</th><th>Status</th><th>Date / source</th></tr></thead><tbody>')
        for ev in evidence:
            output.append('<tr><td>'+E(ev.get('label',''))+'</td><td>'+E(ev.get('result',''))+'</td><td>'+E(ev.get('status',''))+'</td><td>'+E(ev.get('checked_at',''))+' '+E(ev.get('source',''))+'</td></tr>')
        output.append('</tbody></table></section>')
    output.append('<section class="sec" id="portals"><h2>03 · Official website lookup guide</h2><p class="help">Official sources checked as links on 2026-11-03; recheck current forms, menus and access when using them. No automatic data is sent by this checklist.</p><table class="link-table"><thead><tr><th>Portal</th><th>What you enter / where to click</th></tr></thead><tbody>')
    for name,url,instructions,pid in PORTALS:
        output.append('<tr><td><a target="_blank" rel="noopener noreferrer" href="'+E(url)+'">'+E(name)+'</a> <small>'+E(pid)+'</small></td><td>'+E(instructions)+'</td></tr>')
    output.append('</tbody></table><p class="note">Privacy: ask the current owner for any OTP-controlled challans, insurance claim records, and proprietary service history. NCRB and police no-match searches have limited coverage and do not certify accident-free history.</p></section>')
    section_no=4
    for section,rows in groups.items():
        output.append('<section class="sec" id="'+E(section.lower().replace(' ','-').replace('/','-'))+'"><h2>'+f'{section_no:02d}'+' · '+E(section)+' <small>'+str(len(rows))+' checks</small></h2>')
        if 'DIESEL / CNG / EV' in section: output.append('<p class="help">Select “Not applicable” for systems not fitted to this vehicle. Inspection of high-voltage systems is for qualified technicians only.</p>')
        output.append(render_checks(rows))
        output.append('</section>');section_no+=1
    output.append('<section class="sec"><h2>'+f'{section_no:02d}'+' · Inspector observations and pending follow-up</h2><textarea class="longnotes" id="global_notes" data-persist placeholder="Inspection date; inspector / garage; measurements; source links; missing documents; seller commitments; repair estimate; conflicts">'+E(data.get('notes',''))+'</textarea><p class="note">Outcome statement should distinguish: VERIFIED official records / user-supplied documents / image observations / blocked searches / unexplained conflicts. A price recommendation is a separate, user-requested analysis.</p></section>')
    output.append('</div><footer class="foot">Independent evidence checklist · No login required · The page makes no network requests · Save progress as JSON · Print > Save as PDF (A4)</footer></main><script>'+SCRIPT+'</script></body></html>')
    return ''.join(output)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data',type=Path,default=ROOT/'templates/vehicle-data.json')
    parser.add_argument('--checks',type=Path,default=ROOT/'templates/checks.json')
    parser.add_argument('--output',type=Path,default=ROOT/'output/Reusable_Used_Vehicle_Checklist.html')
    args=parser.parse_args()
    data=json.loads(args.data.read_text(encoding='utf-8'))
    checks=json.loads(args.checks.read_text(encoding='utf-8'))
    if len({x['id'] for x in checks})!=len(checks): raise SystemExit('Duplicate checklist ids')
    html_doc=render(data,checks)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html_doc,encoding='utf-8')
    print(f'Wrote {args.output} ({len(checks)} checks, {len(PORTALS)} lookup links, {len(html_doc):,} chars)')

if __name__=='__main__':main()