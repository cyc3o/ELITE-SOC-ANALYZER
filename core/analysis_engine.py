# =====================================================
# ELITE SOC ANALYZER v7.0 — INDUSTRY CLOSED LOOP ENGINE
# AUTHOR: VISHAL — SOC ENGINEERING (L5+)
# =====================================================

import os
import hashlib
from collections import defaultdict
from datetime import datetime, timedelta

import config as cfg

from core.parser import LogParser
from intelligence.threat_intel import ThreatIntelligence
from core.ml_engine import MLAnomalyDetector
from core.risk_engine import (
    calculate_risk_score,
    calculate_confidence_level
)
from core.mitre import MITRE_ATTACK

from storage.database import (
    init_db,
    upsert_incident
)

from ui.ui import display_status, display_warning, display_error, progress_bar


# =====================================================
# ANALYSIS ENGINE
# =====================================================

class AnalysisEngine:
    """
    SOC v7 Engine
    - Deterministic detection
    - Incident lifecycle aware
    - Cognitive feedback compatible
    - Timeline ready
    """

    def __init__(
        self,
        experience_memory=None,
        defender_brain=None,
        time_engine=None,
        mutation_engine=None
    ):
        # Core systems
        self.parser = LogParser()
        self.threat_intel = ThreatIntelligence()
        self.ml = MLAnomalyDetector()

        # Cognitive systems (optional)
        self.memory = experience_memory
        self.defender = defender_brain
        self.time_engine = time_engine
        self.mutation = mutation_engine

        # Init DB once
        init_db()

        # Runtime stats
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

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def analyze_file(self, file_path: str):
        if not os.path.isfile(file_path):
            display_error(f"FILE NOT FOUND: {file_path}")
            return []

        self.stats["ANALYSIS_START"] = datetime.utcnow()
        display_status(f"STARTING ANALYSIS: {file_path}")

        events = self._parse_file(file_path)

        if cfg.ENABLE_ML_ANOMALY_DETECTION:
            self.ml.build_baseline(events)

        alerts = self._correlate(events)

        if cfg.ENABLE_ALERT_DEDUPLICATION:
            alerts = self._deduplicate(alerts)

        alerts = self._apply_time_pressure(alerts)
        self._apply_cognitive_feedback(alerts)
        self._finalize_stats(alerts)

        return alerts

    # =====================================================
    # PARSING
    # =====================================================

    def _parse_file(self, file_path):
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

                if idx % 250 == 0:
                    progress_bar(idx, self.stats["TOTAL_LINES"], "PARSING")

        progress_bar(self.stats["TOTAL_LINES"], self.stats["TOTAL_LINES"], "PARSING")
        return events

    # =====================================================
    # CORRELATION
    # =====================================================

    def _correlate(self, events):
        alerts = []
        ip_map = defaultdict(list)
        user_map = defaultdict(list)

        for e in events:
            if e.get("ip"):
                ip_map[e["ip"]].append(e)
            if e.get("user"):
                user_map[e["user"]].append(e)

        for ip, evs in ip_map.items():
            alerts.extend(self._analyze_ip(ip, evs))

        for user, evs in user_map.items():
            alerts.extend(self._analyze_user(user, evs))

        return alerts

    # =====================================================
    # IP ANALYSIS
    # =====================================================

    def _analyze_ip(self, ip, events):
        alerts = []
        now = datetime.utcnow()
        window = timedelta(minutes=cfg.FAILED_LOGIN_WINDOW_MINUTES)

        recent = []
        for e in events:
            try:
                if datetime.fromisoformat(e["INGEST_TIME"]) > now - window:
                    recent.append(e)
            except Exception:
                continue

        failed = sum(1 for e in recent if "FAILED" in e.get("EVENT_TYPE", ""))
        success = sum(1 for e in events if "ACCEPTED" in e.get("EVENT_TYPE", ""))

        threats, _ = self.threat_intel.check_ip_reputation(ip)
        geo = self.threat_intel.get_geoip_info(ip)

        ml_score = 0
        if cfg.ENABLE_ML_ANOMALY_DETECTION:
            ml_score = self.ml.detect_anomalies(ip, events)
            if ml_score >= cfg.ANOMALY_THRESHOLD:
                self.stats["ML_ANOMALIES_DETECTED"] += 1

        pain_bias = self.memory.pain_index() if self.memory else 0

        if cfg.ENABLE_FP_REDUCTION:
            if success >= cfg.FP_SUCCESSFUL_LOGIN_THRESHOLD and \
               failed < cfg.FAILED_LOGIN_THRESHOLD and \
               pain_bias < 0.3:
                self.stats["FALSE_POSITIVES_SUPPRESSED"] += 1
                return alerts

        if failed >= cfg.FAILED_LOGIN_THRESHOLD:
            risk = calculate_risk_score(
                failed_attempts=failed,
                geo_risk=geo.get("COUNTRY") in cfg.GEO_RISK_COUNTRIES,
                threat_intel=bool(threats),
                ml_anomaly_score=ml_score
            )

            if self.time_engine and self.time_engine.breach_clock > 0.6:
                risk = min(risk + 10, cfg.MAX_RISK_SCORE)

            confidence = calculate_confidence_level(
                data_quality=0.9,
                threat_intel_match=bool(threats),
                behavioral_consistency=0.6 if ml_score > 0.5 else 1.0
            )

            mitre = MITRE_ATTACK.get("SSH_BRUTE_FORCE", {})

            alert = {
                "ALERT_ID": self._alert_id(ip),
                "INCIDENT_STATE": "OPEN",
                "CATEGORY": "AUTHENTICATION",
                "THREAT_TYPE": "SSH_BRUTE_FORCE",
                "THREAT_LEVEL": self._classify_threat(risk),
                "SOURCE_IP": ip,
                "FAILED_ATTEMPTS": failed,
                "SUCCESSFUL_LOGINS": success,
                "RISK_SCORE": risk,
                "CONFIDENCE": confidence,
                "ML_ANOMALY_SCORE": round(ml_score, 2),
                "GEO_COUNTRY": geo.get("COUNTRY"),
                "FIRST_SEEN": events[0]["INGEST_TIME"],
                "LAST_SEEN": events[-1]["INGEST_TIME"],
                "MITRE_ATTACK": mitre,
                "KILL_CHAIN_PHASE": mitre.get("TACTIC"),
                "ALERT_SOURCE": cfg.TOOL_NAME,
                "TOOL_VERSION": cfg.TOOL_VERSION
            }

            upsert_incident(alert)
            alerts.append(alert)

        return alerts

    # =====================================================
    # USER ANALYSIS
    # =====================================================

    def _analyze_user(self, user, events):
        alerts = []
        ips = {e.get("ip") for e in events if e.get("ip")}

        if len(ips) >= 4:
            mitre = MITRE_ATTACK.get("ACCOUNT_COMPROMISE", {})
            alert = {
                "ALERT_ID": self._alert_id(user),
                "INCIDENT_STATE": "OPEN",
                "CATEGORY": "LATERAL_MOVEMENT",
                "THREAT_TYPE": "POTENTIAL_ACCOUNT_COMPROMISE",
                "USERNAME": user,
                "UNIQUE_IPS": list(ips),
                "IP_COUNT": len(ips),
                "THREAT_LEVEL": "MEDIUM",
                "RISK_SCORE": 60,
                "CONFIDENCE": 70,
                "MITRE_ATTACK": mitre,
                "KILL_CHAIN_PHASE": mitre.get("TACTIC"),
                "ALERT_SOURCE": cfg.TOOL_NAME
            }

            upsert_incident(alert)
            alerts.append(alert)

        return alerts

    # =====================================================
    # TIME & COGNITION
    # =====================================================

    def _apply_time_pressure(self, alerts):
        if not self.time_engine:
            return alerts

        if self.time_engine.breach_clock > cfg.BREACH_PROBABILITY_WARNING:
            for a in alerts:
                if a["THREAT_LEVEL"] == "HIGH":
                    a["THREAT_LEVEL"] = "CRITICAL"
        return alerts

    def _apply_cognitive_feedback(self, alerts):
        if not self.mutation:
            return

        for a in alerts:
            if a["THREAT_LEVEL"] == "CRITICAL":
                self.mutation.observe_success()
            elif a["THREAT_LEVEL"] == "MEDIUM":
                self.mutation.observe_regret(
                    {"alert": a["THREAT_TYPE"], "reason": "uncertain"}
                )

    # =====================================================
    # DEDUP
    # =====================================================

    def _deduplicate(self, alerts):
        unique = []
        seen = {}
        window = timedelta(minutes=cfg.ALERT_DEDUP_WINDOW_MINUTES)

        for a in alerts:
            key = (a.get("THREAT_TYPE"), a.get("SOURCE_IP"))
            now = datetime.utcnow()
            if key in seen and now - seen[key] < window:
                continue
            seen[key] = now
            unique.append(a)

        return unique

    # =====================================================
    # HELPERS
    # =====================================================

    def _alert_id(self, seed):
        return hashlib.md5(
            f"{seed}_{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:12]

    def _classify_threat(self, risk):
        if risk >= 80:
            return "CRITICAL"
        if risk >= 60:
            return "HIGH"
        return "MEDIUM"

    def _finalize_stats(self, alerts):
        self.stats["ANALYSIS_END"] = datetime.utcnow()
        self.stats["ANALYSIS_TIME"] = (
            self.stats["ANALYSIS_END"] - self.stats["ANALYSIS_START"]
        ).total_seconds()

        self.stats["THREATS_DETECTED"] = len(alerts)
        self.stats["CRITICAL_THREATS"] = sum(1 for a in alerts if a["THREAT_LEVEL"] == "CRITICAL")
        self.stats["HIGH_THREATS"] = sum(1 for a in alerts if a["THREAT_LEVEL"] == "HIGH")
        self.stats["MEDIUM_THREATS"] = sum(1 for a in alerts if a["THREAT_LEVEL"] == "MEDIUM")