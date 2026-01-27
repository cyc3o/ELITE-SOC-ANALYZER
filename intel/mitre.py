# =====================================================
# ELITE SOC — MITRE ATT&CK ENGINE
# AUTHOR: VISHAL — SOC ENGINEERING
# =====================================================

from collections import defaultdict
from datetime import datetime
from typing import Dict, List


# ==================== HEATMAP ====================

def build_tactic_heatmap(alerts: List[Dict]) -> Dict[str, int]:
    """
    Build MITRE tactic heatmap from alerts
    """
    heatmap = defaultdict(int)

    for alert in alerts:
        tactic = alert.get("KILL_CHAIN_PHASE") or "UNKNOWN"
        heatmap[tactic] += 1

    return dict(heatmap)


# ==================== TECHNIQUE MAP ====================

def build_technique_map(alerts: List[Dict]) -> Dict[str, int]:
    """
    Count MITRE techniques across alerts
    """
    techniques = defaultdict(int)

    for alert in alerts:
        mitre = alert.get("MITRE_ATTACK", {})
        technique_id = mitre.get("TECHNIQUE_ID")
        if technique_id:
            techniques[technique_id] += 1

    return dict(techniques)


# ==================== TIMELINE ====================

def build_attack_timeline(alerts: List[Dict]) -> List[Dict]:
    """
    Build ordered MITRE attack timeline
    """
    timeline = []

    for alert in alerts:
        timeline.append({
            "time": alert.get("FIRST_SEEN"),
            "tactic": alert.get("KILL_CHAIN_PHASE", "UNKNOWN"),
            "technique": (
                alert.get("MITRE_ATTACK", {}).get("TECHNIQUE_ID")
            ),
            "threat": alert.get("THREAT_TYPE"),
            "severity": alert.get("THREAT_LEVEL")
        })

    return sorted(
        timeline,
        key=lambda x: x.get("time") or datetime.utcnow().isoformat()
    )


# ==================== SUMMARY ====================

def mitre_summary(alerts: List[Dict]) -> Dict:
    """
    Full MITRE summary for SOC UI / reports
    """
    return {
        "TACTIC_HEATMAP": build_tactic_heatmap(alerts),
        "TECHNIQUE_COUNTS": build_technique_map(alerts),
        "TOTAL_ALERTS": len(alerts)
    }