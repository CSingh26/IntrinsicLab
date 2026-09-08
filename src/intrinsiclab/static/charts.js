const fmt=(v)=>new Intl.NumberFormat('en-US',{maximumFractionDigits:1}).format(v);
const safe=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function forecastChart(data){
  const rows=data.valuation.forecast,discounted=data.valuation.discounted_fcff;
  const width=800,height=270,left=62,top=25,bottom=220,right=780;
  const values=rows.flatMap((r,i)=>[r.fcff,discounted[i]]),lo=Math.min(0,...values),hi=Math.max(1,...values);
  const range=hi-lo, y=v=>bottom-(v-lo)/range*(bottom-top), band=(right-left)/rows.length;
  let svg=`<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Annual free cash flows and their present values in ${safe(data.currency)} millions"><title>Cash available versus present value</title>`;
  for(let i=0;i<5;i++){const v=lo+range*i/4;svg+=`<line x1="${left}" y1="${y(v)}" x2="${right}" y2="${y(v)}" stroke="#e4eae6"/><text x="${left-10}" y="${y(v)+4}" text-anchor="end" fill="#61777e" font-size="11">${fmt(v)}</text>`;}
  svg+=`<line x1="${left}" y1="${y(0)}" x2="${right}" y2="${y(0)}" stroke="#a5b7b0"/>`;
  rows.forEach((row,i)=>{const x=left+i*band+band*.22,w=Math.min(32,band*.24);[row.fcff,discounted[i]].forEach((v,j)=>{const title=`${row.year}: ${j?'Present value':'FCFF'} ${data.currency} ${fmt(v)} million`;svg+=`<rect x="${x+j*(w+4)}" y="${Math.min(y(v),y(0))}" width="${w}" height="${Math.max(1,Math.abs(y(v)-y(0)))}" rx="2" fill="${j?'#a6cabb':'#216e55'}" tabindex="0"><title>${safe(title)}</title></rect>`;});svg+=`<text x="${left+i*band+band*.5}" y="244" text-anchor="middle" fill="#61777e" font-size="11">${row.year}</text>`;});
  return `<div class="chart"><div class="legend"><span><i class="dot" style="background:#216e55"></i>Free cash flow</span><span><i class="dot" style="background:#a6cabb"></i>Discounted to today</span><span>${safe(data.currency)} millions</span></div>${svg}</svg></div>`;
}
function valueBridge(data){
  const v=data.valuation,m=data.assumptions,values=[['Explicit cash flows',v.discounted_fcff.reduce((a,b)=>a+b,0)],['Terminal value (PV)',v.discounted_terminal_value],['Enterprise value',v.enterprise_value],['Debt',-m.debt],['Preferred / NCI',-m.preferred_equity-m.noncontrolling_interests],['Nonoperating cash',m.cash],['Equity residual',v.equity_value]];
  return `<div class="chart"><h3>The enterprise-to-equity bridge</h3><table><caption>${safe(data.currency)} millions · Asset value reconciled to capital claims</caption><tbody>${values.map(([k,val])=>`<tr><td>${k}</td><td>${fmt(val)}</td></tr>`).join('')}</tbody></table></div>`;
}
document.addEventListener('valuation-rendered',e=>{
  const data=e.detail;document.querySelector('#forecast-chart').innerHTML=forecastChart(data);document.querySelector('#value-bridge').innerHTML=valueBridge(data);
  const cells=[...document.querySelectorAll('.sensitivity-cell')],values=data.sensitivity.rows.flatMap(r=>r.values.map(c=>c.price)).filter(p=>p!=null),low=Math.min(...values),high=Math.max(...values);
  cells.forEach(cell=>{const v=Number(cell.textContent.replaceAll(',',''));if(!Number.isFinite(v))return;const strength=high===low?.25:.08+.5*(v-low)/(high-low);cell.style.background=`rgba(48,135,96,${strength})`;cell.tabIndex=0;});
});
