"""
CORE INTELLIGENCE LOOP – THE THINKING HEART
------------------------------------------
This loop forces Attacker, Defender, and Time
to argue until the least-wrong truth emerges.

Nothing is trusted blindly.
Everything must justify its existence.
"""

from datetime import datetime
import uuid


class IntelligenceState:
    """
    Represents a single cycle of collective intelligence.
    """

    def __init__(self):
        self.cycle_id = str(uuid.uuid4())
        self.started_at = datetime.utcnow()
        self.attacker_view = None
        self.defender_view = None
        self.time_view = None
        self.final_truth = None

    def snapshot(self):
        return {
            "cycle_id": self.cycle_id,
            "started_at": self.started_at.isoformat(),
            "attacker_view": self.attacker_view,
            "defender_view": self.defender_view,
            "time_view": self.time_view,
            "final_truth": self.final_truth
        }


class CoreIntelligenceLoop:
    """
    Coordinates all brains.
    Forces disagreement.
    Extracts convergence.
    """

    def __init__(self, attacker_brain, defender_brain, time_engine):
        self.attacker = attacker_brain
        self.defender = defender_brain
        self.time = time_engine
        self.history = []

    def run_cycle(self, environment_context):
        """
        Run one full intelligence cycle.
        """

        state = IntelligenceState()

        # 1. Attacker predicts future intent
        attacker_prediction = self.attacker.think_next_move(environment_context)
        state.attacker_view = attacker_prediction

        # 2. Defender evaluates with doubt
        defender_decision = self.defender.evaluate_threat(
            attacker_prediction,
            environment_context
        )
        state.defender_view = defender_decision

        # 3. Time engine evaluates trajectory
        temporal_risk = self.time.analyze_temporal_risk()
        breach_window = self.time.predict_breach_window()

        state.time_view = {
            "temporal_risk": temporal_risk,
            "breach_window": breach_window,
            "time_warning": self.time.time_based_warning()
        }

        # 4. Forced disagreement resolution
        state.final_truth = self._synthesize_truth(
            attacker_prediction,
            defender_decision,
            temporal_risk
        )

        self.history.append(state)
        return state.snapshot()

    def _synthesize_truth(self, attacker, defender, temporal):
        """
        This is where magic happens.
        No single brain is trusted.
        """

        attacker_conf = attacker.get("confidence", 0)
        defender_conf = defender.get("confidence", 0)
        breach_prob = temporal.get("breach_probability", 0)

        # Weighted reality model
        reality_score = (
            (attacker_conf * 0.4) +
            (defender_conf * 0.3) +
            (breach_prob * 0.3)
        )

        if reality_score < 0.3:
            verdict = "Observe silently. Risk exists but action now causes more harm."

        elif reality_score < 0.6:
            verdict = (
                "Investigate selectively. Prepare containment. "
                "Time is neutral but may soon favor attacker."
            )

        else:
            verdict = (
                "Immediate action required. "
                "Converged intelligence indicates imminent compromise."
            )

        return {
            "reality_score": round(reality_score, 2),
            "verdict": verdict,
            "philosophy": (
                "Truth emerges from disagreement, "
                "not from certainty."
            )
        }

    def predict_system_failure(self):
        """
        Predicts if the intelligence loop itself is becoming blind.
        """
        if len(self.history) < 5:
            return "Insufficient cycles to evaluate system health."

        high_conf_cycles = [
            h for h in self.history
            if h.final_truth and h.final_truth["reality_score"] > 0.8
        ]

        if len(high_conf_cycles) > len(self.history) * 0.6:
            return (
                "System confidence saturation detected. "
                "Risk of collective blind spot increasing."
            )

        return "Collective intelligence health within acceptable bounds."

    def memory_snapshot(self):
        """
        Full system self-awareness snapshot.
        """
        return {
            "cycles_completed": len(self.history),
            "recent_cycles": [h.snapshot() for h in self.history[-3:]],
            "system_health": self.predict_system_failure()
        }


# SAFE STANDALONE DEMO
if __name__ == "__main__":
    from brains.attacker.attacker_brain import AttackerBrain
    from brains.defender.defender_brain import DefenderBrain
    from brains.time.time_engine import TimeEngine

    attacker = AttackerBrain()
    defender = DefenderBrain()
    time_engine = TimeEngine()

    # Spawn attacker persona
    attacker.spawn_attacker()

    core = CoreIntelligenceLoop(attacker, defender, time_engine)

    environment = {
        "exposed_services": ["RDP", "VPN"],
        "user_risk_score": 78,
        "business_impact": "high",
        "alert_noise": 60,
        "threat_intel_match": False
    }

    cycle_result = core.run_cycle(environment)
    print("[INTELLIGENCE CYCLE RESULT]")
    print(cycle_result)

    system_state = core.memory_snapshot()
    print("[SYSTEM MEMORY]")
    print(system_state)