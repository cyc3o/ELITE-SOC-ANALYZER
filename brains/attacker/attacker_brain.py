"""
ATTACKER BRAIN – FUTURE-GRADE SOC ENGINE
---------------------------------------
This module simulates attacker thinking, intent, evolution,
and next-move prediction without executing real attacks.

Purpose:
- Predict attacker behavior
- Simulate unknown attack paths
- Think like adversaries BEFORE they act
"""

import random
import uuid
from datetime import datetime


class AttackerProfile:
    """
    Represents an attacker persona.
    """

    def __init__(self, skill_level, motivation, patience):
        self.id = str(uuid.uuid4())
        self.skill_level = skill_level        # low / medium / high / nation-state
        self.motivation = motivation          # money / access / sabotage / espionage
        self.patience = patience              # fast / slow / sleeper
        self.created_at = datetime.utcnow()

    def describe(self):
        return {
            "attacker_id": self.id,
            "skill_level": self.skill_level,
            "motivation": self.motivation,
            "patience": self.patience,
            "created_at": self.created_at.isoformat()
        }


class AttackHypothesis:
    """
    Represents a possible attack path that may or may not happen.
    """

    def __init__(self, vector, confidence, reasoning):
        self.vector = vector                  # phishing, credential abuse, lateral move
        self.confidence = confidence          # probability score
        self.reasoning = reasoning
        self.generated_at = datetime.utcnow()

    def explain(self):
        return {
            "attack_vector": self.vector,
            "confidence": round(self.confidence, 2),
            "reasoning": self.reasoning,
            "generated_at": self.generated_at.isoformat()
        }


class AttackerBrain:
    """
    The core attacker simulation engine.
    Thinks like an adversary, not like a rule.
    """

    POSSIBLE_VECTORS = [
        "phishing_initial_access",
        "credential_reuse",
        "living_off_the_land",
        "lateral_movement",
        "privilege_escalation",
        "data_exfiltration",
        "persistence_setup"
    ]

    def __init__(self):
        self.active_profiles = []
        self.generated_hypotheses = []

    def spawn_attacker(self):
        """
        Create a new attacker persona.
        """
        profile = AttackerProfile(
            skill_level=random.choice(["low", "medium", "high"]),
            motivation=random.choice(["financial", "access", "espionage"]),
            patience=random.choice(["fast", "slow", "sleeper"])
        )
        self.active_profiles.append(profile)
        return profile.describe()

    def think_next_move(self, environment_context):
        """
        Predict the next attacker move based on environment weakness.
        """
        vector = random.choice(self.POSSIBLE_VECTORS)

        confidence = self._calculate_confidence(environment_context, vector)

        reasoning = (
            f"Based on exposed services: {environment_context.get('exposed_services')}, "
            f"user behavior risk: {environment_context.get('user_risk_score')}, "
            f"and historical incidents, attacker likely attempts {vector}."
        )

        hypothesis = AttackHypothesis(
            vector=vector,
            confidence=confidence,
            reasoning=reasoning
        )

        self.generated_hypotheses.append(hypothesis)
        return hypothesis.explain()

    def simulate_unknown_attack(self):
        """
        Generate attack logic that does not directly map to known MITRE techniques.
        """
        abstract_vectors = [
            "identity_confusion_chain",
            "trust_boundary_poisoning",
            "slow_permission_drift",
            "shadow_admin_emergence"
        ]

        vector = random.choice(abstract_vectors)

        hypothesis = AttackHypothesis(
            vector=vector,
            confidence=random.uniform(0.4, 0.7),
            reasoning="Pattern does not fully match known frameworks. Generated via behavior anomaly clustering."
        )

        self.generated_hypotheses.append(hypothesis)
        return hypothesis.explain()

    def _calculate_confidence(self, context, vector):
        """
        Internal logic to score probability of success.
        """
        base = 0.3

        if context.get("exposed_services"):
            base += 0.2

        if context.get("user_risk_score", 0) > 70:
            base += 0.2

        if vector in ["credential_reuse", "phishing_initial_access"]:
            base += 0.1

        return min(base + random.uniform(0.0, 0.2), 0.95)

    def memory_snapshot(self):
        """
        Returns everything the attacker brain currently 'believes'.
        """
        return {
            "active_attackers": [p.describe() for p in self.active_profiles],
            "attack_hypotheses": [h.explain() for h in self.generated_hypotheses],
            "hypothesis_count": len(self.generated_hypotheses)
        }


# Standalone test (safe to run)
if __name__ == "__main__":
    brain = AttackerBrain()

    attacker = brain.spawn_attacker()
    print("[+] Spawned attacker:", attacker)

    env = {
        "exposed_services": ["RDP", "SSH"],
        "user_risk_score": 82
    }

    prediction = brain.think_next_move(env)
    print("[+] Predicted next move:", prediction)

    unknown = brain.simulate_unknown_attack()
    print("[+] Unknown attack hypothesis:", unknown)

    snapshot = brain.memory_snapshot()
    print("[+] Brain memory snapshot:", snapshot)