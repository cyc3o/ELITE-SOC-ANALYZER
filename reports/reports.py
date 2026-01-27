# =====================================================
# ELITE SOC ANALYZER v4.0 — REPORTING & IOC ENGINE
# AUTHOR: VISHAL - SOC ENGINEERING
# =====================================================

import os
import json
import csv
import hashlib
from datetime import datetime
from collections import defaultdict

from config import REPORT_DIR, IOC_EXPORT_DIR
from ui.ui import display_status, display_warning

# ==================== IOC EXTRACTION ====================

class IOCExtractor:
    """
    EXTRACT INDICATORS OF COMPROMISE FROM ALERTS
    (IPs, USERS, TOR, DOMAINS, HASHES)
    """

    @staticmethod
    def extract_iocs(alerts):
        iocs = {
            "IPS": set(),
            "USERS": set(),
            "DOMAINS": set(),
            "HASHES": set(),
            "TOR_NODES": set()
        }

        for alert in alerts:
            # SOURCE IP
            if alert.get("SOURCE_IP"):
                iocs["IPS"].add(alert["SOURCE_IP"])

            # USERNAME
            if alert.get("USERNAME"):
                iocs["USERS"].add(alert["USERNAME"])

            # TOR DETECTION FROM THREAT INTEL
            for intel in alert.get("THREAT_INTEL", []):
                if "TOR" in intel:
                    if alert.get("SOURCE_IP"):
                        iocs["TOR_NODES"].add(alert["SOURCE_IP"])

        return {
            "IPS": list(iocs["IPS"]),
            "USERS": list(iocs["USERS"]),
            "DOMAINS": list(iocs["DOMAINS"]),
            "HASHES": list(iocs["HASHES"]),
            "TOR_NODES": list(iocs["TOR_NODES"]),
            "GENERATED_AT": datetime.now().isoformat()
        }

def json_safe(obj):
    """
    CONVERT NON-SERIALIZABLE OBJECTS (datetime → string)
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)



# ==================== REPORT GENERATOR ====================

class ReportGenerator:
    """
    ENTERPRISE SOC REPORT GENERATOR
    OUTPUTS JSON + CSV + IOC FEEDS
    """

    def __init__(self):
        os.makedirs(REPORT_DIR, exist_ok=True)
        os.makedirs(IOC_EXPORT_DIR, exist_ok=True)

    # ==================== MASTER REPORT ====================

    def generate_reports(self, alerts, stats):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_id = hashlib.md5(timestamp.encode()).hexdigest()[:12]

        display_status(f"GENERATING REPORTS | ID: {report_id}")

        self._generate_json(alerts, stats, report_id)
        self._generate_csv(alerts, report_id)
        self._export_iocs(alerts, report_id)

        return report_id

    # ==================== JSON REPORT ====================

    def _generate_json(self, alerts, stats, report_id):
        report = {
            "METADATA": {
                "REPORT_ID": report_id,
                "GENERATED_AT": datetime.now().isoformat()
            },
            "STATISTICS": stats,
            "ALERTS": alerts
        }

        path = os.path.join(
            REPORT_DIR,
            f"ELITE_REPORT_{report_id}.json"
        )

        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, default=json_safe)

        display_status(f"JSON REPORT GENERATED: {path}")

    # ==================== CSV REPORT ====================

    def _generate_csv(self, alerts, report_id):
        if not alerts:
            display_warning("NO ALERTS FOR CSV EXPORT")
            return

        fields = set()
        for alert in alerts:
            for k, v in alert.items():
                if not isinstance(v, (dict, list)):
                    fields.add(k)

        path = os.path.join(
            REPORT_DIR,
            f"ELITE_REPORT_{report_id}.csv"
        )

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=sorted(fields),
                extrasaction="ignore"
            )
            writer.writeheader()

            for alert in alerts:
                writer.writerow(alert)

        display_status(f"CSV REPORT GENERATED: {path}")

    # ==================== IOC EXPORT ====================

    def _export_iocs(self, alerts, report_id):
        iocs = IOCExtractor.extract_iocs(alerts)

        path = os.path.join(
            IOC_EXPORT_DIR,
            f"IOCS_{report_id}.json"
        )

        with open(path, "w", encoding="utf-8") as f:
            json.dump(iocs, f, indent=2)

        display_status(f"IOC FEED EXPORTED: {path}")