# =====================================================
# ELITE SOC ANALYZER v4.0 — ANALYSIS & CORRELATION ENGINE
# AUTHOR: VISHAL - SOC ENGINEERING
# =====================================================

import os
import sys
import hashlib
from collections import defaultdict
from datetime import datetime, timedelta

from parser import LogParser
from threat_intel import ThreatIntelligence
from ml_engine import MLAnomalyDetector
from risk_engine import (
    calculate_risk_score,
    calculate_confidence_level
)
from mitre import MITRE_ATTACK
from ui import (
    display_status,
    display_warning,
    display_error,
    progress_bar
)
from config import (
    FAILED_LOGIN_THRESHOLD,
    FAILED_LOGIN_WINDOW_MINUTES,
    FP_SUCCESSFUL_LOGIN_THRESHOLD,
    ENABLE_FP_REDUCTION,
    ENABLE_ALERT_DEDUPLICATION,
    ALERT_DEDUP_WINDOW_MINUTES,
    GEO_RISK_COUNTRIES,
    ANOMALY_THRESHOLD,
    TOOL_NAME,
    TOOL_VERSION
)

# ==================== ANALYSIS ENGINE ====================

class AnalysisEngine:
    """
    ELITE SOC CORRELATION & THREAT DETECTION ENGINE
    """

    def __init__(self):
        self.parser = LogParser()
        self.threat_intel = ThreatIntelligence()
        self.ml = MLAnomalyDetector()

        self.stats = {
            "TOTAL_LINES": 0,
            "PARSED_EVENTS": 0,
            "THREATS_DETECTED": 0,
            "CRITICAL_THREATS": 0,
            "HIGH_THREATS": 0,
            "MEDIUM_THREATS": 0,
            "ML_ANOMALIES_DETECTED": 0,
            "FALSE_POSITIVES_SUPPRESSED": 0,
            "ANALYSIS_START": None,
            "ANALYSIS_END": None,
            "ANALYSIS_TIME": 0
        }

    # ==================== FILE ANALYSIS ====================

    def analyze_file(self, file_path):
        if not os.path.isfile(file_path):
            display_error(f"FILE NOT FOUND: {file_path}")
            sys.exit(1)

        self.stats["ANALYSIS_START"] = datetime.now()
        display_status(f"STARTING ANALYSIS: {file_path}")

        events = []

        with open(file_path, "r", errors="ignore") as f:
            lines = f.readlines()
            self.stats["TOTAL_LINES"] = len(lines)

            for idx, line in enumerate(lines):
                parsed = self.parser.parse_line(line)
                if parsed:
                    parsed["LINE_NUMBER"] = idx + 1
                    parsed["SOURCE_FILE"] = os.path.basename(file_path)
                    events.append(parsed)
                    self.stats["PARSED_EVENTS"] += 1

                if idx % 100 == 0:
                    progress_bar(idx, self.stats["TOTAL_LINES"], "PARSING")

        progress_bar(
            self.stats["TOTAL_LINES"],
            self.stats["TOTAL_LINES"],
            "PARSING"
        )

        # BUILD ML BASELINE
        self.ml.build_baseline(events)

        display_status("CORRELATING EVENTS")
        alerts = self._correlate(events)

        # ALERT DEDUPLICATION
        if ENABLE_ALERT_DEDUPLICATION:
            alerts = self._deduplicate(alerts)

        self.stats["ANALYSIS_END"] = datetime.now()
        self.stats["ANALYSIS_TIME"] = (
            self.stats["ANALYSIS_END"] - self.stats["ANALYSIS_START"]
        ).total_seconds()

        self.stats["THREATS_DETECTED"] = len(alerts)
        self.stats["CRITICAL_THREATS"] = sum(
            1 for a in alerts if a.get("THREAT_LEVEL") == "CRITICAL"
        )
        self.stats["HIGH_THREATS"] = sum(
            1 for a in alerts if a.get("THREAT_LEVEL") == "HIGH"
        )
        self.stats["MEDIUM_THREATS"] = sum(
            1 for a in alerts if a.get("THREAT_LEVEL") == "MEDIUM"
        )

        return alerts

    # ==================== CORRELATION ====================

    def _correlate(self, events):
        alerts = []
        ip_events = defaultdict(list)
        user_events = defaultdict(list)

        for e in events:
            if "ip" in e:
                ip_events[e["ip"]].append(e)
            if "user" in e:
                user_events[e["user"]].append(e)

        for ip, evs in ip_events.items():
            alerts.extend(self._analyze_ip(ip, evs))

        for user, evs in user_events.items():
            alerts.extend(self._analyze_user(user, evs))

        return alerts

    # ==================== IP ANALYSIS ====================

    def _analyze_ip(self, ip, events):
        alerts = []

        now = datetime.utcnow()
        window = timedelta(minutes=FAILED_LOGIN_WINDOW_MINUTES)

        recent = [
            e for e in events
            if datetime.fromisoformat(e["INGEST_TIME"]) > now - window
        ]

        failed = sum(
            1 for e in recent
            if "FAILED" in e.get("EVENT_TYPE", "")
        )
        success = sum(
            1 for e in events
            if "ACCEPTED" in e.get("EVENT_TYPE", "")
        )
        total = len(events)

        threats, live = self.threat_intel.check_ip_reputation(ip)
        geo = self.threat_intel.get_geoip_info(ip)

        ml_score = self.ml.detect_anomalies(ip, events)
        if ml_score >= ANOMALY_THRESHOLD:
            self.stats["ML_ANOMALIES_DETECTED"] += 1

        # FALSE POSITIVE REDUCTION
        if ENABLE_FP_REDUCTION:
            if success >= FP_SUCCESSFUL_LOGIN_THRESHOLD and failed < 10:
                self.stats["FALSE_POSITIVES_SUPPRESSED"] += 1
                return alerts

        # ==================== SSH BRUTE FORCE ====================

        if failed >= FAILED_LOGIN_THRESHOLD:
            risk = calculate_risk_score(
                failed_attempts=failed,
                geo_risk=geo["COUNTRY"] in GEO_RISK_COUNTRIES,
                threat_intel=bool(threats),
                ml_anomaly_score=ml_score
            )

            confidence = calculate_confidence_level(
                data_quality=0.9,
                threat_intel_match=bool(threats),
                behavioral_consistency=0.5 if ml_score > 0.5 else 1.0
            )

            mitre = MITRE_ATTACK.get("SSH_BRUTE_FORCE", {})

            alerts.append({
                "ALERT_ID": hashlib.md5(
                    f"{ip}_{datetime.now()}".encode()
                ).hexdigest()[:12],
                "THREAT_LEVEL": "CRITICAL" if risk >= 80 else "HIGH",
                "CATEGORY": "AUTHENTICATION",
                "THREAT_TYPE": "SSH_BRUTE_FORCE",
                "SOURCE_IP": ip,
                "FAILED_ATTEMPTS": failed,
                "SUCCESSFUL_LOGINS": success,
                "TOTAL_EVENTS": total,
                "RISK_SCORE": risk,
                "CONFIDENCE": confidence,
                "ML_ANOMALY_SCORE": round(ml_score, 2),
                "THREAT_INTEL": threats,
                "GEO_COUNTRY": geo["COUNTRY"],
                "FIRST_SEEN": events[0]["INGEST_TIME"],
                "LAST_SEEN": events[-1]["INGEST_TIME"],

                # 🔥 MITRE ENRICHMENT
                "MITRE_ATTACK": mitre,
                "KILL_CHAIN_PHASE": mitre.get("TACTIC"),

                "ALERT_SOURCE": TOOL_NAME,
                "TOOL_VERSION": TOOL_VERSION
            })

        return alerts

    # ==================== USER ANALYSIS ====================

    def _analyze_user(self, user, events):
        alerts = []
        ips = set(e.get("ip") for e in events if e.get("ip"))

        if len(ips) >= 4:
            mitre = MITRE_ATTACK.get("ACCOUNT_COMPROMISE", {})

            alerts.append({
                "ALERT_ID": hashlib.md5(
                    f"{user}_{datetime.now()}".encode()
                ).hexdigest()[:12],
                "THREAT_LEVEL": "MEDIUM",
                "CATEGORY": "LATERAL_MOVEMENT",
                "THREAT_TYPE": "POTENTIAL_ACCOUNT_COMPROMISE",
                "USERNAME": user,
                "UNIQUE_IPS": list(ips),
                "IP_COUNT": len(ips),
                "RISK_SCORE": 60,
                "CONFIDENCE": 70,
                "FIRST_SEEN": events[0]["INGEST_TIME"],
                "LAST_SEEN": events[-1]["INGEST_TIME"],
                "MITRE_ATTACK": mitre,
                "KILL_CHAIN_PHASE": mitre.get("TACTIC"),
                "ALERT_SOURCE": TOOL_NAME
            })

        return alerts

    # ==================== ALERT DEDUPLICATION ====================

    def _deduplicate(self, alerts):
        unique = []
        seen = {}
        window = timedelta(minutes=ALERT_DEDUP_WINDOW_MINUTES)

        for a in alerts:
            key = (a.get("THREAT_TYPE"), a.get("SOURCE_IP"))
            now = datetime.now()

            if key in seen and now - seen[key] < window:
                continue

            seen[key] = now
            unique.append(a)

        return unique