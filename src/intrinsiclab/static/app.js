import './charts.js';
const $ = (q) => document.querySelector(q);
const $$ = (q) => [...document.querySelectorAll(q)];
const form = $('#valuation-form');
const rateFields = ['tax_rate','wacc','terminal_growth','terminal_margin','terminal_roic'];
const driverFields = ['growth','operating_margin','da_ratio','capex_ratio','nwc_ratio'];
let model, result, requestId = 0;
const cases = [];
const number = (v, digits=1) => v == null ? 'Unavailable' : new Intl.NumberFormat('en-US',{maximumFractionDigits:digits,minimumFractionDigits:digits}).format(v);
const escape = (s) => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const el = (name) => form.elements.namedItem(name);
function error(message) { $('#error').textContent = message; $('#error').hidden = !message; }
function clearResults() { result = undefined; $('#summary').innerHTML='<p>Assumptions changed. Recalculate to inspect the updated valuation.</p>'; for (const id of ['warnings','forecast','sensitivity','forecast-chart','value-bridge']) $('#'+id).replaceChildren(); $('#export').disabled = true; }
async function api(route, body) {
  const response = await fetch(route, body ? {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)} : {});
  const data = await response.json();
  if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail));
  return data;
}
function download(name, value) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(value,null,2)], {type:'application/json'}));
  const a = document.createElement('a'); a.href=url;a.download=name;a.click();URL.revokeObjectURL(url);
}
async function readJson(file) { if(!file) return; if(file.size>500000) throw new Error('File exceeds 500 KB limit');return JSON.parse(await file.text()); }
function drawDrivers() {
  $('#drivers tbody').innerHTML=model.years.map((row,i)=>`<tr><td>${model.base_year+i+1}</td>${driverFields.map(key=>`<td><input data-year="${i}" data-driver="${key}" aria-label="${model.base_year+i+1} ${key.replaceAll('_',' ')} percent" type="number" step="any" value="${Number((row[key]*100).toFixed(8))}" required></td>`).join('')}</tr>`).join('');
}
function fill(next) {
  model = structuredClone(next);
  for (const key of ['company','currency','base_year','revenue','opening_nwc','terminal_method','exit_multiple','debt','cash','preferred_equity','noncontrolling_interests','shares',...rateFields]) el(key).value=rateFields.includes(key) ? Number((model[key]*100).toFixed(8)) : model[key];
  drawDrivers(); terminalFields(); $('#mode').textContent=model.source.mode; $('#source').textContent=JSON.stringify(model.source,null,2);
}
function terminalFields() { const g=el('terminal_method').value==='gordon';$('#gordon-fields').hidden=!g;$('#exit-field').hidden=g; }
function currentModel() {
  const next=structuredClone(model);
  for (const key of ['company','currency','base_year','revenue','opening_nwc','terminal_method','exit_multiple','debt','cash','preferred_equity','noncontrolling_interests','shares',...rateFields]) {
    const value=el(key).value;
    next[key]=['company','currency','terminal_method'].includes(key) ? value : Number(value)/(rateFields.includes(key)?100:1);
  }
  next.years=model.years.map((_,i)=>Object.fromEntries(driverFields.map(key=>[key,Number($(`[data-year="${i}"][data-driver="${key}"]`).value)/100])));
  return next;
}
function render(data) {
  result=data; const v=data.valuation, currency=escape(data.currency);
  $('#summary').innerHTML=`<article class="metric"><span class="metric-label">BASE-CASE RESIDUAL / SHARE</span><strong>${currency} ${number(v.price_per_share,2)}</strong><p>Modeled equity value ÷ diluted shares</p></article><article class="metric"><span class="metric-label">SENSITIVITY RANGE / SHARE</span><strong>${number(data.sensitivity_range.low,2)} – ${number(data.sensitivity_range.high,2)}</strong><p>${currency} · Across displayed assumption combinations</p></article><article class="metric"><span class="metric-label">VALUE FROM TERMINAL PERIOD</span><strong>${v.terminal_share_of_ev == null ? 'N/M' : number(100*v.terminal_share_of_ev,0)+'%'}</strong><p>Investigate the long-term assumptions</p></article>`;
  $('#warnings').innerHTML=data.warnings.map(w=>`<p>${escape(w)}</p>`).join('');
  const columns=[['revenue','Revenue'],['ebit','EBIT'],['cash_taxes','Cash taxes'],['nopat','NOPAT'],['da','D&A'],['capex','CapEx'],['change_nwc','ΔNWC'],['fcff','FCFF']];
  $('#forecast').innerHTML=`<table><caption>${currency} millions · Annual fiscal periods · End-year discounting</caption><thead><tr><th>Year</th>${columns.map(([,label])=>`<th>${label}</th>`).join('')}</tr></thead><tbody>${v.forecast.map(row=>`<tr><td>${row.year}</td>${columns.map(([key])=>`<td>${number(row[key])}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
  const s=data.sensitivity, growth=s.axis==='terminal_growth';
  $('#sensitivity').innerHTML=`<table><caption>${currency} per share · Rows: WACC · Columns: ${growth?'terminal growth':'exit EV/EBITDA'}</caption><thead><tr><th>WACC ↓ / Terminal →</th>${s.columns.map(c=>`<th>${number(c*(growth?100:1),1)}${growth?'%':'×'}</th>`).join('')}</tr></thead><tbody>${s.rows.map(row=>`<tr><th>${number(row.wacc*100)}%</th>${row.values.map(c=>`<td title="${escape(c.reason||'Recalculated equity value per share')}" class="sensitivity-cell">${c.price==null?'N/A':number(c.price,2)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
  $('#interpretation').textContent=data.interpretation; $('#source').textContent=JSON.stringify({...data.source,model_id:data.model_id,engine_version:data.engine_version,units:data.units},null,2);$('#mode').textContent=data.source.mode;$('#export').disabled=false;
  document.dispatchEvent(new CustomEvent('valuation-rendered',{detail:data}));
}
async function calculate() {
  const id=++requestId; clearResults();error('');$('#calculate').disabled=true;
  try { const next=currentModel(), data=await api('/api/valuations',next);if(id!==requestId) return;model=next;render(data); }
  catch(e) { if(id===requestId) error(e.message); }
  finally { if(id===requestId) $('#calculate').disabled=false; }
}
form.addEventListener('submit',e=>{e.preventDefault();calculate();});
form.addEventListener('input',()=>{++requestId;$('#calculate').disabled=false;clearResults();terminalFields();});
$$('[data-tab]').forEach(button=>button.addEventListener('click',()=>{ $$('[data-tab],.tab').forEach(n=>n.classList.remove('active'));button.classList.add('active');$('#'+button.dataset.tab).classList.add('active');error(''); }));
$('#reset').addEventListener('click',async()=>{try{fill(await api('/api/demo'));await calculate();}catch(e){error(e.message);}});
$('#add-year').addEventListener('click',()=>{if(model.years.length>=15)return;model=currentModel();model.years.push({...model.years.at(-1)});drawDrivers();clearResults();});
$('#remove-year').addEventListener('click',()=>{if(model.years.length<=1)return;model=currentModel();model.years.pop();drawDrivers();clearResults();});
$('#import').addEventListener('change',async e=>{try{const raw=await readJson(e.target.files[0]);if(!raw)return;const next=raw.assumptions||raw;const valid=await api('/api/valuations',next);fill(valid.assumptions);render(valid);error('');}catch(e){clearResults();error('Model unavailable: '+e.message);}});
$('#export').addEventListener('click',()=>{if(result)download('intrinsiclab-evidence.json',result);});
$('#capital-form').addEventListener('submit',async e=>{
  e.preventDefault();$('#capital-result').replaceChildren();error('');
  try {const data=Object.fromEntries([...new FormData(e.target)].map(([k,v])=>[k,Number(v)/(['risk_free_rate','equity_risk_premium','pretax_cost_of_debt','tax_rate'].includes(k)?100:1)]));const r=await api('/api/cost-of-capital',data);
    $('#capital-result').innerHTML=`<h3>WACC ${number(r.wacc*100,2)}%</h3><p>Equity requires ${number(r.cost_of_equity*100,2)}%; after-tax debt costs ${number(r.after_tax_cost_of_debt*100,2)}%. Market financing is ${number(r.equity_weight*100)}% equity.</p><button type="button" id="apply-wacc">Apply WACC to valuation</button>`;
    $('#apply-wacc').disabled=r.wacc<=0||r.wacc>.5;$('#apply-wacc').onclick=()=>{el('wacc').value=r.wacc*100;clearResults();$('[data-tab="valuation"]').click();calculate();};
  }catch(e){error(e.message);}
});
$('#peer-example').onclick=()=>download('intrinsiclab-peers.json',{source:{provider:'Synthetic teaching example',as_of:'2026-09-08',mode:'DEMO DATA'},peers:[{company:'Fictional Peer',currency:'USD',price:20,shares:10,debt:40,cash:10,revenue:100,ebitda:25,net_income:10,book_equity:80}]});
$('#peer-import').onchange=async e=>{try{const payload=await readJson(e.target.files[0]);if(!payload)return;const r=await api('/api/comparables',payload);$('#peer-results').innerHTML=`<p>${escape(r.source.mode)} · ${escape(r.source.provider)}</p><table><thead><tr><th>Company</th><th>P/E</th><th>EV/EBITDA</th><th>EV/Sales</th><th>P/Book</th></tr></thead><tbody>${r.peers.map(p=>`<tr><td>${escape(p.company)}</td>${['pe','ev_ebitda','ev_sales','price_book'].map(k=>`<td title="${escape(p[k].reason||'Multiple')} ">${p[k].value==null?'N/M':number(p[k].value,2)+'×'}</td>`).join('')}</tr>`).join('')}</tbody></table>`;error('');}catch(e){$('#peer-results').replaceChildren();error(e.message);}};
$('#csv-import').onchange=async e=>{try{const file=e.target.files[0];if(!file)return;if(file.size>250000)throw new Error('CSV exceeds 250 KB');const provider=$('#statement-source').value.trim();if(!provider)throw new Error('Enter the statement source before importing');const source={provider,as_of:new Date().toISOString().slice(0,10),mode:'USER INPUT',reference:file.name,retrieved_at:new Date().toISOString(),transformation:'Uploaded annual CSV; millions; no currency conversion'};const r=await api('/api/statements/normalize',{content:await file.text(),source});$('#statement-results').innerHTML=`<pre>${escape(JSON.stringify(r,null,2))}</pre><button id="apply-statements">Apply latest annual base</button>`;$('#apply-statements').onclick=()=>{const row=r.rows.at(-1);model=currentModel();Object.assign(model,{base_year:row.fiscal_year,currency:row.currency,revenue:row.revenue,opening_nwc:row.nwc,source});fill(model);$('[data-tab="valuation"]').click();calculate();};error('');}catch(e){$('#statement-results').replaceChildren();error(e.message);}};
function renderCases(){ $('#cases').innerHTML=cases.map((c,i)=>`<div class="case"><span>${escape(c.assumptions.company)}<br><small>${escape(c.currency)} ${number(c.valuation.price_per_share,2)} / share · WACC ${number(c.assumptions.wacc*100)}%</small></span><button type="button" class="secondary" data-case="${i}">Restore</button></div>`).join('');$$('[data-case]').forEach(b=>b.onclick=()=>{fill(cases[Number(b.dataset.case)].assumptions);calculate();}); }
$('#save-case').onclick=()=>{if(!result){error('Recalculate before saving a case.');return;}if(cases.length>=10){error('This session holds at most 10 cases. Export evidence to keep more.');return;}cases.push(structuredClone(result));renderCases();};
try { fill(await api('/api/demo'));await calculate(); }catch(e){error('Data unavailable: '+e.message);}
