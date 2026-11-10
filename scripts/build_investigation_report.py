#!/usr/bin/env python3
"""Create a full HTML investigation report around the existing 134-point checklist.

python3 scripts/build_investigation_report.py --data investigation.json --output report.html
Optional --embed-images includes non-sensitive local photos.
--include-sensitive-images is an explicit opt-in for authorized private outputs.
"""
import argparse, base64, html, json, mimetypes, re, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
E=lambda x:html.escape(str(x if x is not None else ''),quote=True)

def table(headers,rows):
    if not rows:return '<p class="help">No result recorded.</p>'
    return '<div style="overflow-x:auto"><table class="report-table"><thead><tr>'+''.join('<th>'+E(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def cp(value):
    s=str(value or '').strip()
    return ('<code>'+E(s)+'</code> <button class="copy-value no-print" type="button" data-copy="'+E(s)+'">Copy</button>') if s else '<i>Not verified</i>'

def anchor(url,label='Open official website'):
    return '<a href="'+E(url)+'" target="_blank" rel="noopener noreferrer">'+E(label)+'</a>' if url.startswith('https://') else E(label)

def page(data,portals,base,photo_mode,sensitive_mode,checklist):
    ids=dict(data.get('identifiers') or {})
    vin=str(ids.get('vin') or '').strip().upper().replace(' ','')
    engine=str(ids.get('engine_number') or '').strip().upper().replace(' ','')
    if vin:ids.update(vin_last_5=vin[-5:],vin_last_4=vin[-4:])
    if engine:ids['engine_last_4']=engine[-4:]
    reg=str(ids.get('registration') or 'Not supplied')
    title=data.get('report_title') or 'Detailed Used-Vehicle Investigation'
    red=''.join('<div class="report-alert"><b>'+E(x.get('title'))+'</b><small>'+E(x.get('detail'))+'</small><small>Source: '+E(x.get('evidence'))+'</small></div>' for x in data.get('attention_points',[])) or '<p>No attention points recorded. This is not evidence of a clean vehicle.</p>'
    metrics=data.get('metrics') or [{'label':x,'value':ids.get(y) or 'Not verified'} for x,y in [('Registration','registration'),('First registered','first_registration'),('Owner serial','owner_serial'),('RC validity','registration_valid_to')]]
    ms=''.join('<div class="report-metric"><small>'+E(m.get('label'))+'</small><b>'+E(m.get('value'))+'</b></div>' for m in metrics)
    fields=[('Registration','registration'),('Formatted number','formatted_registration'),('VIN/full chassis','vin'),('VIN last 5','vin_last_5'),('VIN last 4','vin_last_4'),('Engine number','engine_number'),('Engine last 4','engine_last_4'),('Make','make'),('Model','model'),('Variant','variant'),('Fuel','fuel'),('Transmission','transmission'),('Vehicle class','vehicle_class'),('RTO','rto'),('First registered','first_registration'),('Manufacture month','manufacture_month_year'),('Owner serial','owner_serial'),('Owner count','owner_count'),('RC validity','registration_valid_to'),('Odometer','odometer'),('MV tax expiry','mv_tax_valid_to'),('PUC expiry','puc_valid_to'),('HSRP status','hsrp_status'),('Insurer','insurance_company'),('Insurance expiry','insurance_valid_to'),('HP/loan','loan_or_hypothecation'),('Renewal application','renewal_application')]
    ids_rows=[[E(label),cp(ids.get(k)),E((data.get('identifier_evidence') or {}).get(k,'Source unverified'))] for label,k in fields]
    ids_rows += [[E(x.get('label')),cp(x.get('value')),E(x.get('source'))] for x in data.get('additional_identifiers',[])]
    records=[[E(x.get('status')),E(x.get('subject')),E(x.get('result')),E(x.get('source')),E(x.get('checked_at'))] for x in data.get('records',[])]
    observations=[[E(x.get('area')),E(x.get('observation')),E(x.get('limitations')),E(x.get('follow_up')),E(x.get('evidence'))] for x in data.get('observations',[])]
    overrides={x.get('id'):x for x in data.get('portals',[]) if x.get('id')}; pc=[]
    for i,original in enumerate(portals,1):
        p={**original,**overrides.get(original.get('id'),{})}
        if p.get('skip'):continue
        fields_html=''.join('<div class="report-field"><span>'+E(f.get('label'))+'</span>'+cp(ids.get(f['key']) if 'key' in f else f.get('value'))+'</div>' for f in p.get('fields',[]))
        pc.append('<article class="report-card"><h3>'+str(i)+'. '+E(p.get('title'))+'</h3><p><b>Steps:</b> '+E(p.get('steps'))+'</p>'+fields_html+'<p>'+anchor(p.get('url',''))+' | '+E(p.get('status') or 'Not checked')+'</p><small>'+E(p.get('limits'))+'</small></article>')
    remaining=''.join('<article class="report-card"><b>'+E(x.get('title'))+'</b><p>'+E(x.get('detail'))+'</p></article>' for x in data.get('outstanding',[]))
    comps=[[E(x.get('description')),E(x.get('mileage')),E(x.get('asking_price')),anchor(x.get('url',''),'Listing'),E(x.get('checked_at')),E(x.get('caveat'))] for x in data.get('comparables',[])]
    gallery=[]
    for pic in data.get('photos',[]):
        if not photo_mode or (pic.get('sensitive') and not sensitive_mode):continue
        q=Path(pic.get('path',''))
        if not q.is_absolute():q=base/q
        if not q.is_file() or q.stat().st_size>15000000:continue
        mime=mimetypes.guess_type(q.name)[0]
        if mime not in ('image/png','image/jpeg','image/webp','image/gif'):continue
        image='data:'+mime+';base64,'+base64.b64encode(q.read_bytes()).decode('ascii')
        gallery.append('<figure><img src="'+image+'" alt="'+E(pic.get('caption'))+'"><figcaption><b>'+E(pic.get('id'))+'</b> '+E(pic.get('caption'))+'<small>'+E(pic.get('observation'))+'</small></figcaption></figure>')
    evidence=[[E(x.get('id')),E(x.get('source')),E(x.get('result')),E(x.get('date')),E(x.get('limitation'))] for x in data.get('evidence',[])]
    top='''<section class="report-red"><h2>Record flags and unresolved verification — review first</h2><div class="report-grid">'''+red+'''</div><p class="help">A missing search result, insurance claim or police record cannot be treated as proof that a car is accident-free.</p></section>'''
    top+='<div class="report-metrics">'+ms+'</div>'
    top+='<section class="sec"><h2>Vehicle identity and copy-ready details</h2>'+table(['Field','Value to copy','Evidence'],ids_rows)+'</section>'
    top+='<section class="sec"><h2>Online and government investigation records</h2>'+table(['Status','Topic','Exact outcome','Source','Date'],records)+'</section>'
    top+='<section class="sec"><h2>Remote visual observations (not a mechanical inspection)</h2>'+table(['Area','Visible','Limitations','Physical test','Evidence'],observations)+'</section>'
    top+='<section class="sec"><h2>Official website field-by-field guide</h2><p class="help">Verify live menu names, use the listed plate/VIN only when known, enter CAPTCHA manually and do not bypass owner OTP.</p><div class="report-grid">'+''.join(pc)+'</div></section>'
    top+='<section class="sec"><h2>Outstanding seller and inspector evidence</h2><div class="report-grid">'+remaining+'</div></section>'
    top+='<section class="sec"><h2>Current comparable listings (asking prices only)</h2>'+table(['Vehicle','Mileage','Asking price','Link','Checked','Limitations'],comps)+'</section>'
    top+='<section class="sec"><h2>Photographic evidence</h2><p class="help">Sensitive RC/identity photos are omitted unless explicitly authorized for a private report.</p><div class="report-gallery">'+''.join(gallery)+'</div></section>'
    top+='<section class="sec"><h2>Evidence ledger</h2>'+table(['ID','Source','Finding','Date','Limitations'],evidence)+'</section>'
    css='''<style>.report-red{background:#fff1f1;border:1px solid #e7b6bd;border-left:6px solid #b32635;border-radius:7px;margin:16px 0;padding:15px}.report-red h2{color:#a52935}.report-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.report-alert,.report-card{border:1px solid #dce5ea;border-radius:6px;padding:10px;background:#fff;break-inside:avoid}.report-alert{border-color:#ecd4d7}.report-alert b,.report-alert small{display:block}.report-alert small{font-size:11px;margin-top:4px;color:#65717a}.report-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.report-metric{border:1px solid #dbe2e8;padding:9px;border-radius:6px}.report-metric small,.report-metric b{display:block}.report-metric b{font-size:16px}.report-table{border-collapse:collapse;width:100%;font-size:11px}.report-table td,.report-table th{border-bottom:1px solid #e1e9ed;text-align:left;padding:7px 9px;vertical-align:top}.report-table th{background:#edf4f7}.report-field{display:flex;justify-content:space-between;gap:7px;border-bottom:1px dashed #dce5ea;padding:4px 0;font-size:11px}.report-card h3{font-size:14px;margin:0 0 6px;color:#215063}.report-card p,.report-card small{font-size:11px}.copy-value{font-size:10px;padding:2px 6px;border:1px solid #97c0c8;border-radius:3px;background:white;color:#00586c}.report-gallery{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}.report-gallery figure{margin:0;border:1px solid #dde6ea}.report-gallery img{width:100%;height:185px;object-fit:cover}.report-gallery figcaption{padding:6px;font-size:10px}.report-gallery figcaption small{display:block;color:#65717a}@media(max-width:650px){.report-grid{grid-template-columns:1fr}.report-metrics{grid-template-columns:1fr 1fr}.report-gallery{grid-template-columns:1fr}}@media print{.report-grid{grid-template-columns:1fr 1fr}.report-gallery img{height:100px}.copy-value{display:none}.report-card{break-inside:avoid}.report-table td,.report-table th{padding:5px;font-size:9px}}</style>'''
    # Add before the existing independent checklist; 134-point interactive controls remain operational.
    checklist=checklist.replace('</head>',css+'</head>',1)
    checklist=checklist.replace('<div class="content">','<div class="content">'+top,1)
    checklist=checklist.replace('Second-Hand Vehicle Verification and Inspection Checklist',E(title),2)
    checklist=checklist.replace('</body>','<script>document.addEventListener("click",async e=>{let b=e.target.closest("[data-copy]");if(!b)return;let v=b.dataset.copy;try{await navigator.clipboard.writeText(v)}catch{let a=document.createElement("textarea");a.value=v;document.body.append(a);a.select();document.execCommand("copy");a.remove()}b.textContent="Copied";setTimeout(()=>b.textContent="Copy",900)});</script></body>',1)
    return checklist

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data',required=True,type=Path);ap.add_argument('--output',required=True,type=Path)
    ap.add_argument('--portals',type=Path,default=ROOT/'templates/portal-checks.json')
    ap.add_argument('--embed-images',action='store_true');ap.add_argument('--include-sensitive-images',action='store_true')
    a=ap.parse_args();d=json.loads(a.data.read_text(encoding='utf-8'));portals=json.loads(a.portals.read_text(encoding='utf-8'))
    base=d.get('identifiers') or {}
    checklist_data={'report_title':d.get('report_title','Vehicle investigation'), 'report_date':d.get('report_date',''), 'identifiers':base,'recorded_flags':[{'label':f.get('title',''),'detail':f.get('detail',''),'source':f.get('evidence','')} for f in d.get('attention_points',[])], 'evidence':d.get('evidence',[])}
    with tempfile.TemporaryDirectory() as tmp:
        inp=Path(tmp)/'vehicle.json';out=Path(tmp)/'checklist.html';inp.write_text(json.dumps(checklist_data),encoding='utf-8')
        subprocess.run([sys.executable,str(ROOT/'scripts/build_checklist.py'),'--data',str(inp),'--output',str(out)],check=True,capture_output=True,text=True)
        checklist=out.read_text(encoding='utf-8')
    result=page(d,portals,a.data.parent,a.embed_images,a.include_sensitive_images,checklist)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(result,encoding='utf-8')
    print('Wrote',a.output,'and retained 134 checklist controls')
if __name__=='__main__': main()
