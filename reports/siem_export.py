# =====================================================
# ELITE SOC ANALYZER — SOC L5 SIEM EXPORT ENGINE
# AUTHOR: VISHAL - SOC ENGINEERING
# =====================================================

import os
import json
import uuid
from datetime import datetime, timezone

from config import REPORT_DIR
from ui.ui import display_status

# ==================== HELPERS ====================

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def severity_to_numeric(level):
    """
    Normalize severity to SIEM scale (0–10)
    """
    return {
        "CRITICAL": 9,
        "HIGH": 7,
        "MEDIUM": 5,
        "LOW": 3
    }.get(level, 1)

# ==================== SIEM EXPORT ====================

class SIEMExporter:
    """
    SOC L5 SIEM-NORMALIZED EXPORT
    (Splunk / ELK / Sentinel compatible)
    """

    def __init__(self):
        os.makedirs(REPORT_DIR, exist_ok=True)

    def export(self, alerts, report_id):
        display_status("EXPORTING SIEM-NORMALIZED EVENTS")

        siem_file = os.path.join(
            REPORT_DIR,
            f"SIEM_EVENTS_{report_id}.ndjson"
        )

        with open(siem_file, "w", encoding="utf-8") as f:
            for alert in alerts:
                event = self._normalize(alert, report_id)
                f.write(json.dumps(event) + "\n")

        display_status(f"SIEM EXPORT GENERATED: {siem_file}")
        return siem_file

    # ==================== NORMALIZATION ====================

    def _normalize(self, alert, report_id):
        mitre = alert.get("MITRE_ATTACK", {})

        return {
            # Core SIEM fields
            "event.id": alert.get("ALERT_ID", str(uuid.uuid4())),
            "event.kind": "alert",
            "event.category": alert.get("CATEGORY", "security"),
            "event.type": alert.get("THREAT_TYPE", "unknown"),
            "event.severity": severity_to_numeric(
                alert.get("THREAT_LEVEL")
            ),
            "event.risk_score": alert.get("RISK_SCORE", 0),
            "event.confidence": alert.get("CONFIDENCE", 0),
            "event.created": utc_now(),
            "event.dataset": "elite_soc",

            # Source / user
            "source.ip": alert.get("SOURCE_IP"),
            "user.name": alert.get("USERNAME"),

            # Geo
            "source.geo.country_name": alert.get("GEO_COUNTRY"),

            # MITRE ATT&CK (flattened for SIEM)
            "threat.framework": "MITRE ATT&CK",
            "threat.tactic.name": mitre.get("TACTIC"),
            "threat.technique.id": mitre.get("TECHNIQUE"),
            "threat.technique.name": mitre.get("TECHNIQUE_NAME"),

            # ML
            "ml.anomaly_score": alert.get("ML_ANOMALY_SCORE"),

            # Tool metadata
            "observer.vendor": "ELITE_SOC",
            "observer.type": "SOC_ANALYZER",
            "observer.version": alert.get("TOOL_VERSION"),
            "report.id": report_id,

            # Raw enrichment
            "threat.intel": alert.get("THREAT_INTEL", []),
            "first_seen": alert.get("FIRST_SEEN"),
            "last_seen": alert.get("LAST_SEEN")
        }