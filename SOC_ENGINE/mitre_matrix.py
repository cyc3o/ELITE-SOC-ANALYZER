# =====================================================
# ELITE SOC ANALYZER — MITRE ATT&CK MATRIX EXPORT
# AUTHOR: VISHAL - SOC ENGINEERING
# =====================================================

import json
import os
from collections import defaultdict
from datetime import datetime
from config import REPORT_DIR
from ui import display_status

class MitreMatrixGenerator:
    """
    GENERATE MITRE ATT&CK COVERAGE MATRIX (JSON)
    """

    @staticmethod
    def generate(alerts, report_id):
        tactics = defaultdict(list)

        for alert in alerts:
            mitre = alert.get("MITRE_ATTACK", {})
            tactic = mitre.get("TACTIC")
            technique = mitre.get("TECHNIQUE")

            if tactic and technique:
                tactics[tactic].append({
                    "TECHNIQUE": technique,
                    "NAME": mitre.get("TECHNIQUE_NAME"),
                    "THREAT_TYPE": alert.get("THREAT_TYPE")
                })

        matrix = {
            "GENERATED_AT": datetime.now().isoformat(),
            "TACTICS": dict(tactics)
        }

        os.makedirs(REPORT_DIR, exist_ok=True)
        path = os.path.join(
            REPORT_DIR, f"MITRE_MATRIX_{report_id}.json"
        )

        with open(path, "w", encoding="utf-8") as f:
            json.dump(matrix, f, indent=2)

        display_status(f"MITRE MATRIX GENERATED: {path}")
        return path