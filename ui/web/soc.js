
const ALERTS_URL = "data/alerts.json";
const TIMELINES_URL = "data/timelines.json";
const REFRESH_INTERVAL = 5000;

document.addEventListener("DOMContentLoaded", () => {
  loadAlerts();
  setInterval(loadAlerts, REFRESH_INTERVAL);
});

function loadAlerts() {
  fetch(ALERTS_URL).then(r=>r.json()).then(alerts=>{
    const tbody = document.querySelector("#alerts tbody");
    if(!tbody) return;
    tbody.innerHTML="";
    alerts.forEach(a=>{
      const tr=document.createElement("tr");
      tr.innerHTML=`
        <td>${a.THREAT_LEVEL}</td>
        <td>${a.THREAT_TYPE}</td>
        <td>${a.SOURCE_IP || a.USERNAME || "-"}</td>
        <td>${a.INCIDENT_STATE}</td>
        <td>
          <button onclick="setState('${a.ALERT_ID}','ACK')">ACK</button>
          <button onclick="setState('${a.ALERT_ID}','CLOSED')">CLOSE</button>
          <button onclick="showTimeline('${a.ALERT_ID}')">TIMELINE</button>
        </td>`;
      tbody.appendChild(tr);
    });
  });
}

function setState(id, state){
  fetch(ALERTS_URL).then(r=>r.json()).then(alerts=>{
    alerts.forEach(a=>{
      if(a.ALERT_ID===id){
        a.INCIDENT_STATE=state;
        a.LAST_UPDATED=new Date().toISOString();
      }
    });
    const blob=new Blob([JSON.stringify(alerts,null,2)],{type:"application/json"});
    const a=document.createElement("a");
    a.href=URL.createObjectURL(blob);
    a.download="alerts.json";
    a.click();
  });
}

function showTimeline(id){
  fetch(TIMELINES_URL).then(r=>r.json()).then(tl=>{
    alert(JSON.stringify(tl[id] || [], null, 2));
  });
}
