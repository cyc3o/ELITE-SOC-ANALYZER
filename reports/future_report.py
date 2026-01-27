"""
FUTURE REPORT ENGINE – EXECUTIVE & SOC INTELLIGENCE NARRATIVE
------------------------------------------------------------
This module converts raw intelligence into:
- Human-readable truth
- Executive shock statements
- SOC-actionable guidance
- Future-risk storytelling

Philosophy:
People don’t act on data.
They act on understanding.
"""

from datetime import datetime
import uuid


class FutureReport:
    """
    Represents a single future-facing security report.
    """

    def __init__(self, title):
        self.report_id = str(uuid.uuid4())
        self.title = title
        self.created_at = datetime.utcnow()
        self.sections = []

    def add_section(self, heading, content, severity="info"):
        """
        Add a report section.
        """
        self.sections.append({
            "heading": heading,
            "content": content,
            "severity": severity
        })

    def generate(self):
        """
        Generate full structured report.
        """
        return {
            "report_id": self.report_id,
            "title": self.title,
            "generated_at": self.created_at.isoformat(),
            "sections": self.sections
        }


class FutureReportEngine:
    """
    Builds reports from the intelligence organism.
    """

    def generate_report(
        self,
        intelligence_snapshot,
        defender_snapshot,
        time_snapshot,
        memory_snapshot,
        evolution_snapshot
    ):
        report = FutureReport(
            title="Future Risk Intelligence Assessment"
        )

        # 1. Executive Summary
        report.add_section(
            "Executive Summary",
            self._executive_summary(
                intelligence_snapshot,
                time_snapshot
            ),
            severity="critical"
        )

        # 2. Current Reality
        report.add_section(
            "Current Security Reality",
            self._current_reality(intelligence_snapshot, defender_snapshot),
            severity="high"
        )

        # 3. Attacker Outlook
        report.add_section(
            "Attacker Future Outlook",
            self._attacker_outlook(intelligence_snapshot),
            severity="high"
        )

        # 4. Defender Weakness Projection
        report.add_section(
            "Defensive Failure Projection",
            self._defender_projection(defender_snapshot),
            severity="high"
        )

        # 5. Time-Based Risk
        report.add_section(
            "Time as a Weapon",
            self._time_risk(time_snapshot),
            severity="critical"
        )

        # 6. Experience & Pain Memory
        report.add_section(
            "Lessons Written in Pain",
            self._experience_insights(memory_snapshot),
            severity="medium"
        )

        # 7. Evolution State
        report.add_section(
            "System Evolution Status",
            self._evolution_status(evolution_snapshot),
            severity="info"
        )

        # 8. Final Truth
        report.add_section(
            "Final Intelligence Verdict",
            self._final_verdict(intelligence_snapshot, time_snapshot),
            severity="critical"
        )

        return report.generate()

    # -------- SECTION BUILDERS -------- #

    def _executive_summary(self, intel, time):
        score = intel.get("final_truth", {}).get("reality_score", 0)
        breach = time.get("breach_clock", 0)

        if breach > 0.6:
            return (
                "The organization is on a trajectory toward a security breach. "
                "This assessment is based on converged attacker intent, defender uncertainty, "
                "and time-amplified risk accumulation."
            )

        if score > 0.5:
            return (
                "Security posture is deteriorating. While no breach has occurred, "
                "current trends indicate increasing attacker advantage over time."
            )

        return (
            "No immediate breach trajectory detected. However, absence of evidence "
            "does not indicate absence of threat."
        )

    def _current_reality(self, intel, defender):
        return {
            "attacker_confidence": intel.get("attacker_view", {}).get("confidence"),
            "defender_action": defender.get("recent_decisions", [{}])[-1],
            "system_bias": defender.get("trust_baseline")
        }

    def _attacker_outlook(self, intel):
        attacker = intel.get("attacker_view", {})
        return (
            f"Predicted attacker vector: {attacker.get('attack_vector')}. "
            "This prediction is probabilistic and may evolve as environment changes."
        )

    def _defender_projection(self, defender):
        return (
            "Defensive decisions show signs of cognitive drift. "
            "Without corrective adaptation, probability of missed detection increases."
            if defender.get("trust_baseline", 0.5) > 0.7
            else
            "Defender caution remains within acceptable limits."
        )

    def _time_risk(self, time):
        return {
            "breach_probability": time.get("breach_clock"),
            "time_warning": time.get("last_analysis")
        }

    def _experience_insights(self, memory):
        return {
            "pain_index": memory.get("pain_index"),
            "wisdom": memory.get("wisdom")
        }

    def _evolution_status(self, evolution):
        return evolution.get("status")

    def _final_verdict(self, intel, time):
        return {
            "verdict": intel.get("final_truth", {}).get("verdict"),
            "philosophy": "The future is not random. It is shaped by ignored signals."
        }


# SAFE STANDALONE DEMO
if __name__ == "__main__":
    engine = FutureReportEngine()

    report = engine.generate_report(
        intelligence_snapshot={
            "attacker_view": {
                "attack_vector": "credential_reuse",
                "confidence": 0.72
            },
            "final_truth": {
                "reality_score": 0.67,
                "verdict": "Immediate action required."
            }
        },
        defender_snapshot={
            "trust_baseline": 0.78,
            "recent_decisions": [{"action": "ignore"}]
        },
        time_snapshot={
            "breach_clock": 0.74,
            "last_analysis": "Critical temporal risk"
        },
        memory_snapshot={
            "pain_index": 0.62,
            "wisdom": "Ignoring weak signals has caused damage before."
        },
        evolution_snapshot={
            "status": "Mid evolution – intelligence stabilizing."
        }
    )

    print("[FUTURE REPORT]")
    print(report)