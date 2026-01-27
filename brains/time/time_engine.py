"""
TIME ENGINE – FUTURE-GRADE SECURITY TEMPORAL INTELLIGENCE
--------------------------------------------------------
This engine understands attacks across time, not moments.

Core beliefs:
- Breaches are processes, not events
- Time increases attacker advantage
- Silence over time is a signal
- Future risk is measurable
"""

from datetime import datetime, timedelta
import uuid


class TemporalEvent:
    """
    Represents a security-relevant event anchored in time.
    """

    def __init__(self, event_type, severity, description):
        self.id = str(uuid.uuid4())
        self.event_type = event_type
        self.severity = severity          # 1–10
        self.description = description
        self.timestamp = datetime.utcnow()

    def describe(self):
        return {
            "event_id": self.id,
            "type": self.event_type,
            "severity": self.severity,
            "description": self.description,
            "timestamp": self.timestamp.isoformat()
        }


class TimeEngine:
    """
    Thinks like time itself.
    Understands drift, delay, silence, and accumulation.
    """

    def __init__(self):
        self.timeline = []
        self.breach_clock = 0.0            # 0.0 – 1.0 probability
        self.last_analysis = datetime.utcnow()

    def record_event(self, event_type, severity, description):
        event = TemporalEvent(event_type, severity, description)
        self.timeline.append(event)
        return event.describe()

    def analyze_temporal_risk(self):
        """
        Converts timeline into future breach probability.
        """
        if not self.timeline:
            return self._no_data_forecast()

        now = datetime.utcnow()
        decay_window = timedelta(days=14)

        risk = 0.0

        for event in self.timeline:
            age = now - event.timestamp

            if age > decay_window:
                continue

            weight = (decay_window - age).total_seconds() / decay_window.total_seconds()
            risk += (event.severity / 10) * weight

        self.breach_clock = min(risk, 1.0)

        return {
            "breach_probability": round(self.breach_clock, 2),
            "time_analyzed": now.isoformat(),
            "risk_interpretation": self._interpret_risk(self.breach_clock)
        }

    def predict_breach_window(self):
        """
        Predicts WHEN a breach becomes likely if nothing changes.
        """
        if self.breach_clock < 0.3:
            return "No breach window detected in near future."

        if self.breach_clock < 0.6:
            return "Breach likelihood increases within 7–14 days if no intervention occurs."

        return "Critical: Breach highly probable within 72 hours without corrective action."

    def detect_slow_attack(self):
        """
        Detects long, low-noise attacks.
        """
        low_severity_events = [
            e for e in self.timeline if e.severity <= 4
        ]

        if len(low_severity_events) >= 5:
            return {
                "slow_attack_detected": True,
                "description": (
                    "Multiple low-severity events over extended time indicate "
                    "slow attacker progression or stealth persistence."
                )
            }

        return {
            "slow_attack_detected": False,
            "description": "No temporal stealth pattern detected."
        }

    def defender_time_failure(self, defender_snapshot):
        """
        Predicts when defender behavior becomes dangerous.
        """
        trust = defender_snapshot.get("trust_baseline", 0.5)
        decisions = defender_snapshot.get("total_decisions", 0)

        if decisions > 10 and trust > 0.7:
            return (
                "Defender overconfidence detected. "
                "Probability of missed breach increases over time."
            )

        if decisions > 15 and trust < 0.3:
            return (
                "Defender fatigue detected. "
                "High chance of delayed response in next incident window."
            )

        return "Defender temporal stability within acceptable bounds."

    def time_based_warning(self):
        """
        Human-readable future warning sentence.
        """
        if self.breach_clock < 0.3:
            return "System stability maintained. No immediate future threat trajectory detected."

        if self.breach_clock < 0.6:
            return (
                "Warning: Security posture degrading over time. "
                "Delayed action may see attacker advantage increase."
            )

        return (
            "CRITICAL: Time is now the attacker’s primary weapon. "
            "Immediate intervention required to avoid breach."
        )

    def _interpret_risk(self, risk):
        if risk < 0.3:
            return "Low temporal risk"
        if risk < 0.6:
            return "Elevated temporal risk"
        return "Critical temporal risk"

    def _no_data_forecast(self):
        return {
            "breach_probability": 0.0,
            "interpretation": (
                "No timeline data. Absence of evidence is not evidence of absence."
            )
        }

    def memory_snapshot(self):
        """
        Full temporal state.
        """
        return {
            "events_recorded": len(self.timeline),
            "breach_clock": round(self.breach_clock, 2),
            "last_analysis": self.last_analysis.isoformat(),
            "recent_events": [e.describe() for e in self.timeline[-5:]]
        }


# Safe standalone test
if __name__ == "__main__":
    time_engine = TimeEngine()

    time_engine.record_event(
        event_type="suspicious_login_pattern",
        severity=4,
        description="Repeated failed logins over multiple days"
    )

    time_engine.record_event(
        event_type="credential_misuse_signal",
        severity=6,
        description="Unusual authentication success from rare location"
    )

    analysis = time_engine.analyze_temporal_risk()
    print("[TEMPORAL RISK]", analysis)

    window = time_engine.predict_breach_window()
    print("[BREACH WINDOW]", window)

    slow = time_engine.detect_slow_attack()
    print("[SLOW ATTACK]", slow)

    warning = time_engine.time_based_warning()
    print("[TIME WARNING]", warning)