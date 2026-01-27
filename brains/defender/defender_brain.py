"""
DEFENDER BRAIN – UNBEATABLE EDITION
----------------------------------
This module represents a thinking defender, not a rule engine.

Core philosophy:
- Every alert can be wrong
- Every decision has cost
- Confidence must be justified
- Ignorance must be tracked
"""

import uuid
from datetime import datetime


class DefenderJudgement:
    """
    Represents a single defensive decision with reasoning, doubt, and consequences.
    """

    def __init__(self, action, confidence, reasoning, ignored_signals):
        self.id = str(uuid.uuid4())
        self.action = action                      # investigate / contain / ignore / observe
        self.confidence = confidence              # 0.0 – 1.0
        self.reasoning = reasoning
        self.ignored_signals = ignored_signals
        self.created_at = datetime.utcnow()

    def explain(self):
        return {
            "decision_id": self.id,
            "action": self.action,
            "confidence": round(self.confidence, 2),
            "reasoning": self.reasoning,
            "ignored_signals": self.ignored_signals,
            "timestamp": self.created_at.isoformat()
        }


class DefenderBrain:
    """
    Thinks like a senior SOC lead.
    Never blindly trusts alerts.
    """

    def __init__(self):
        self.decisions = []
        self.regret_memory = []       # Tracks decisions that aged badly
        self.trust_baseline = 0.5     # How much the system trusts itself

    def evaluate_threat(self, attacker_hypothesis, environment_context):
        """
        Evaluate an attacker hypothesis and decide what to do.
        """

        risk = attacker_hypothesis.get("confidence", 0.0)
        vector = attacker_hypothesis.get("attack_vector", "unknown")

        business_impact = environment_context.get("business_impact", "medium")
        detection_noise = environment_context.get("alert_noise", 50)

        confidence = self._calculate_confidence(risk, detection_noise)

        action = self._decide_action(confidence, business_impact)

        ignored = self._identify_ignored_signals(attacker_hypothesis, environment_context)

        reasoning = (
            f"Attack vector '{vector}' evaluated with risk {risk}. "
            f"Business impact assessed as {business_impact}. "
            f"Alert noise level at {detection_noise}. "
            f"Chosen action '{action}' balances risk, cost, and uncertainty."
        )

        decision = DefenderJudgement(
            action=action,
            confidence=confidence,
            reasoning=reasoning,
            ignored_signals=ignored
        )

        self.decisions.append(decision)
        return decision.explain()

    def self_critique(self):
        """
        Defender questions its own past decisions.
        """
        critiques = []

        for d in self.decisions[-5:]:
            if d.confidence > 0.8:
                critiques.append(
                    f"Decision {d.id} may be overconfident. "
                    "High confidence reduces learning opportunities."
                )

            if d.action == "ignore":
                critiques.append(
                    f"Decision {d.id} ignored a signal. "
                    "Future correlation may increase risk."
                )

        return critiques

    def record_regret(self, decision_id, outcome):
        """
        Stores painful lessons when reality proves the defender wrong.
        """
        regret = {
            "decision_id": decision_id,
            "outcome": outcome,
            "recorded_at": datetime.utcnow().isoformat()
        }
        self.regret_memory.append(regret)

        # Reduce blind trust
        self.trust_baseline = max(self.trust_baseline - 0.05, 0.2)

    def predict_future_failure(self):
        """
        Predicts where the defender itself is most likely to fail.
        """
        if not self.decisions:
            return "Insufficient data to predict defender failure."

        ignore_count = sum(1 for d in self.decisions if d.action == "ignore")

        if ignore_count > len(self.decisions) * 0.4:
            return (
                "High probability of future breach due to excessive alert suppression. "
                "Defender bias toward silence detected."
            )

        return "No immediate systemic defensive failure predicted."

    def _calculate_confidence(self, risk, noise):
        """
        Confidence is LOWER when noise is high.
        """
        confidence = risk * (1 - noise / 100)
        confidence = max(min(confidence, 0.95), 0.1)
        return confidence

    def _decide_action(self, confidence, impact):
        """
        Decide action based on uncertainty, not fear.
        """
        if impact == "high" and confidence > 0.4:
            return "contain"

        if confidence > 0.6:
            return "investigate"

        if confidence < 0.25:
            return "observe"

        return "ignore"

    def _identify_ignored_signals(self, hypothesis, context):
        """
        Defender explicitly admits what it is choosing to ignore.
        """
        ignored = []

        if not context.get("threat_intel_match"):
            ignored.append("No external threat intel confirmation")

        if hypothesis.get("confidence", 0) < 0.5:
            ignored.append("Low attacker confidence score")

        if context.get("alert_noise", 0) > 70:
            ignored.append("High alert noise environment")

        return ignored

    def memory_snapshot(self):
        """
        Complete internal defender state.
        """
        return {
            "total_decisions": len(self.decisions),
            "trust_baseline": round(self.trust_baseline, 2),
            "regret_events": len(self.regret_memory),
            "recent_decisions": [d.explain() for d in self.decisions[-3:]]
        }


# Safe standalone execution
if __name__ == "__main__":
    defender = DefenderBrain()

    attacker_prediction = {
        "attack_vector": "credential_reuse",
        "confidence": 0.68
    }

    environment = {
        "business_impact": "high",
        "alert_noise": 65,
        "threat_intel_match": False
    }

    decision = defender.evaluate_threat(attacker_prediction, environment)
    print("[DEFENDER DECISION]", decision)

    critique = defender.self_critique()
    print("[SELF CRITIQUE]", critique)

    failure = defender.predict_future_failure()
    print("[FUTURE FAILURE PREDICTION]", failure)

    snapshot = defender.memory_snapshot()
    print("[DEFENDER MEMORY]", snapshot)