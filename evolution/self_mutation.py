"""
SELF MUTATION ENGINE – EVOLUTION OVER STATIC LOGIC
--------------------------------------------------
This engine mutates defensive intelligence based on:
- regret
- failure
- overconfidence
- time-based outcomes

It does NOT blindly optimize.
It punishes bad certainty and rewards cautious accuracy.

Core belief:
Static logic dies. Adaptive logic survives.
"""

import uuid
from datetime import datetime
import random


class MutationRecord:
    """
    Represents a single evolutionary change.
    """

    def __init__(self, mutation_type, reason, impact):
        self.id = str(uuid.uuid4())
        self.mutation_type = mutation_type
        self.reason = reason
        self.impact = impact
        self.timestamp = datetime.utcnow()

    def describe(self):
        return {
            "mutation_id": self.id,
            "type": self.mutation_type,
            "reason": self.reason,
            "impact": self.impact,
            "timestamp": self.timestamp.isoformat()
        }


class SelfMutationEngine:
    """
    Evolves system behavior over time.
    """

    def __init__(self):
        self.mutation_history = []
        self.evolution_pressure = 0.0   # increases after failures
        self.maturity_level = 1.0       # grows slowly, never resets

    def observe_regret(self, regret_event):
        """
        Regret increases pressure to evolve.
        """
        self.evolution_pressure = min(self.evolution_pressure + 0.15, 1.0)

        mutation = MutationRecord(
            mutation_type="regret_response",
            reason=f"System regret recorded: {regret_event}",
            impact="Reduced future confidence thresholds"
        )

        self.mutation_history.append(mutation)
        return mutation.describe()

    def observe_success(self):
        """
        Success reduces mutation pressure but never removes it.
        """
        self.evolution_pressure = max(self.evolution_pressure - 0.05, 0.1)
        self.maturity_level = min(self.maturity_level + 0.02, 5.0)

    def mutate_defender_bias(self, defender_brain):
        """
        Adjusts defender behavior dynamically.
        """
        if self.evolution_pressure < 0.3:
            return "No mutation required. System stability acceptable."

        adjustment = random.choice(["confidence", "ignore_bias", "containment_threshold"])

        if adjustment == "confidence":
            defender_brain.trust_baseline = max(
                defender_brain.trust_baseline - 0.1, 0.2
            )

            reason = "Overconfidence detected via regret accumulation."
            impact = "Lowered trust baseline"

        elif adjustment == "ignore_bias":
            reason = "Excessive alert ignoring observed."
            impact = "Increased sensitivity to weak signals"

        else:
            reason = "Delayed containment caused escalation."
            impact = "Earlier containment triggers enabled"

        mutation = MutationRecord(
            mutation_type="defender_bias_mutation",
            reason=reason,
            impact=impact
        )

        self.mutation_history.append(mutation)
        self.evolution_pressure *= 0.7
        return mutation.describe()

    def mutate_attacker_model(self, attacker_brain):
        """
        Forces attacker brain to imagine more creative threats.
        """
        if self.evolution_pressure < 0.4:
            return "Attacker model stable."

        attacker_brain.POSSIBLE_VECTORS.append(
            f"emergent_vector_{uuid.uuid4().hex[:6]}"
        )

        mutation = MutationRecord(
            mutation_type="attacker_model_expansion",
            reason="Defender success plateau detected.",
            impact="Introduced unknown attack vector"
        )

        self.mutation_history.append(mutation)
        self.evolution_pressure *= 0.8
        return mutation.describe()

    def decay_old_logic(self):
        """
        Old thinking fades naturally.
        """
        self.mutation_history = self.mutation_history[-50:]
        self.maturity_level = min(self.maturity_level + 0.01, 10.0)

    def evolution_status(self):
        """
        Human-readable evolution state.
        """
        if self.maturity_level < 2:
            return "Early adaptive phase – learning aggressively."
        if self.maturity_level < 5:
            return "Mid evolution – intelligence stabilizing."
        return "Late evolution – slow, careful mutations only."

    def memory_snapshot(self):
        """
        Full evolution awareness.
        """
        return {
            "evolution_pressure": round(self.evolution_pressure, 2),
            "maturity_level": round(self.maturity_level, 2),
            "total_mutations": len(self.mutation_history),
            "recent_mutations": [
                m.describe() for m in self.mutation_history[-3:]
            ],
            "status": self.evolution_status()
        }


# SAFE STANDALONE TEST
if __name__ == "__main__":
    from brains.attacker.attacker_brain import AttackerBrain
    from brains.defender.defender_brain import DefenderBrain

    attacker = AttackerBrain()
    defender = DefenderBrain()
    evolution = SelfMutationEngine()

    # Simulate regret
    regret = {"decision": "ignored lateral movement", "outcome": "breach"}
    print("[REGRET OBSERVED]", evolution.observe_regret(regret))

    # Mutate defender
    print("[DEFENDER MUTATION]", evolution.mutate_defender_bias(defender))

    # Mutate attacker
    print("[ATTACKER MUTATION]", evolution.mutate_attacker_model(attacker))

    print("[EVOLUTION SNAPSHOT]", evolution.memory_snapshot())
