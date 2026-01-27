"""
EXPERIENCE MEMORY – HUMAN-LIKE SECURITY MEMORY
----------------------------------------------
This module stores EXPERIENCE, not logs.

Principles:
- Logs record events
- Memory records pain
- Wisdom comes from remembering consequences
- Repetition without learning is failure
"""

import uuid
from datetime import datetime


class Experience:
    """
    Represents a lived security experience.
    """

    def __init__(
        self,
        category,
        trigger,
        decision,
        outcome,
        lesson,
        severity
    ):
        self.id = str(uuid.uuid4())
        self.category = category              # breach / near-miss / false-positive / success
        self.trigger = trigger                # what started it
        self.decision = decision              # what defender/system did
        self.outcome = outcome                # what actually happened
        self.lesson = lesson                  # what should be remembered
        self.severity = severity              # 1–10
        self.timestamp = datetime.utcnow()

    def describe(self):
        return {
            "experience_id": self.id,
            "category": self.category,
            "trigger": self.trigger,
            "decision": self.decision,
            "outcome": self.outcome,
            "lesson": self.lesson,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat()
        }


class ExperienceMemory:
    """
    Stores and recalls lived security experiences.
    """

    def __init__(self):
        self.memories = []

    def record_experience(
        self,
        category,
        trigger,
        decision,
        outcome,
        lesson,
        severity
    ):
        """
        Record a meaningful security experience.
        """
        exp = Experience(
            category=category,
            trigger=trigger,
            decision=decision,
            outcome=outcome,
            lesson=lesson,
            severity=severity
        )

        self.memories.append(exp)
        return exp.describe()

    def recall_similar(self, trigger_keyword):
        """
        Recall past experiences similar to current situation.
        """
        matches = [
            m.describe()
            for m in self.memories
            if trigger_keyword.lower() in str(m.trigger).lower()
        ]

        return {
            "matches_found": len(matches),
            "experiences": matches
        }

    def pain_index(self):
        """
        Measures accumulated pain.
        """
        if not self.memories:
            return 0.0

        pain = sum(
            m.severity for m in self.memories
            if m.category in ["breach", "near-miss"]
        )

        max_possible = len(self.memories) * 10
        return round(pain / max_possible, 2)

    def wisdom_statement(self):
        """
        Generates a human-readable wisdom line.
        """
        if not self.memories:
            return "No lived experience yet. System is naive."

        repeated_mistakes = len([
            m for m in self.memories
            if "ignored" in str(m.decision).lower()
        ])

        if repeated_mistakes >= 3:
            return (
                "Pattern detected: repeated ignoring of weak signals "
                "has historically resulted in damage."
            )

        return "Experience memory stable. No dominant destructive pattern detected."

    def forget_irrelevant(self):
        """
        Forget low-impact memories over time.
        """
        self.memories = [
            m for m in self.memories
            if m.severity >= 3
        ]

    def memory_snapshot(self):
        """
        Full memory awareness.
        """
        return {
            "total_experiences": len(self.memories),
            "pain_index": self.pain_index(),
            "wisdom": self.wisdom_statement(),
            "recent_experiences": [
                m.describe() for m in self.memories[-3:]
            ]
        }


# SAFE STANDALONE TEST
if __name__ == "__main__":
    memory = ExperienceMemory()

    memory.record_experience(
        category="near-miss",
        trigger="credential reuse detected late",
        decision="ignored early alert",
        outcome="attacker gained limited access",
        lesson="Weak identity signals must not be ignored",
        severity=7
    )

    memory.record_experience(
        category="false-positive",
        trigger="automated scan spike",
        decision="investigated deeply",
        outcome="no malicious activity",
        lesson="High noise events need faster dismissal",
        severity=3
    )

    recall = memory.recall_similar("credential")
    print("[RECALL]", recall)

    snapshot = memory.memory_snapshot()
    print("[MEMORY SNAPSHOT]", snapshot)