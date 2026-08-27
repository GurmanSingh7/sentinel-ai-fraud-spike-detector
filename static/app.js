const $=x=>document.getElementById(x);
const ids=["txn_count","avg_amount","failed_rate","new_device_rate","high_risk_country_rate","chargeback_rate","fraud_rate_baseline","hour"];
const scenarios={
 safe:[420,1800,.03,.12,.03,.01,.01,14],
 review:[900,6500,.14,.48,.15,.06,.025,2],
 spike:[1700,14000,.34,.78,.42,.18,.035,3]
};
function scenario(name){ids.forEach((id,i)=>$(id).value=scenarios[name][i]);}
async function loadMetrics(){
 const m=await fetch("/api/metrics").then(r=>r.json());
 for(const [a,b] of [["precision","precision"],["recall","recall"],["f1","f1"],["p2","precision"],["r2","recall"],["f2","f1"]])
   $(a).textContent=(m[b]*100).toFixed(1)+"%";
 $("fp").textContent=m.confusion_matrix.fp;
 $("cost").textContent="Estimated demo cost: ₹"+Number(m.false_positive_cost).toLocaleString("en-IN");
 $("matrix").innerHTML=`<span>TN <b>${m.confusion_matrix.tn}</b></span><span>FP <b>${m.confusion_matrix.fp}</b></span><span>FN <b>${m.confusion_matrix.fn}</b></span><span>TP <b>${m.confusion_matrix.tp}</b></span>`;
}
$("form").addEventListener("submit",async e=>{
 e.preventDefault();
 const payload={};ids.forEach(id=>payload[id]=Number($(id).value));
 const btn=document.querySelector(".run");btn.disabled=true;btn.innerHTML="ANALYZING WINDOW…";
 try{const d=await fetch("/api/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)}).then(r=>r.json());render(d);}
 catch(e){alert("Could not reach the server.");}
 btn.disabled=false;btn.innerHTML='ANALYZE FRAUD SPIKE <span>→</span>';
});
function render(d){
 $("empty").classList.add("hidden");$("output").classList.remove("hidden");
 $("risk").textContent=Math.round(d.risk_score);$("prob").textContent=(d.fraud_probability*100).toFixed(1)+"%";
 $("fill").style.width=d.risk_score+"%";$("decision").textContent=d.decision;$("decision").className="decision "+d.decision.toLowerCase();
 $("action").textContent=d.recommended_action;$("gmv").textContent="₹"+Number(d.window_gmv).toLocaleString("en-IN",{maximumFractionDigits:0});
 $("signals").innerHTML=d.signals.length?d.signals.map(s=>`<div class="signal"><span>${s.reason}</span><b>${s.impact}</b></div>`).join(""):'<div class="signal"><span>No strong anomaly crossed the explanation threshold</span><b>LOW</b></div>';
}
loadMetrics();
