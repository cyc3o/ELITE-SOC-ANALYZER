
import json
import os
from datetime import datetime

def _json_safe(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)

def export_dashboard_data(alerts, stats):
    os.makedirs("ui/web/data", exist_ok=True)

    for a in alerts:
        a.setdefault("INCIDENT_STATE", "OPEN")
        a.setdefault("ASSIGNED_TO", None)
        a.setdefault("LAST_UPDATED", datetime.now())

    with open("ui/web/data/alerts.json", "w") as f:
        json.dump(alerts, f, indent=2, default=_json_safe)

    with open("ui/web/data/stats.json", "w") as f:
        json.dump(stats, f, indent=2, default=_json_safe)

    timelines = {}
    for a in alerts:
        iid = a.get("ALERT_ID")
        timelines[iid] = [
            {"time": a.get("FIRST_SEEN"), "event": "first_seen"},
            {"time": a.get("LAST_SEEN"), "event": "last_seen"}
        ]

    with open("ui/web/data/timelines.json", "w") as f:
        json.dump(timelines, f, indent=2, default=_json_safe)
