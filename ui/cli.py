"""
MASTER CLI – LIVING SECURITY INTELLIGENCE ORGANISM
-------------------------------------------------
This CLI orchestrates the entire system:
- Attacker Brain
- Defender Brain
- Time Engine
- Core Intelligence Loop
- Experience Memory
- Self Mutation
- Future Report

One command. One truth.
"""

import argparse
import json
from pprint import pprint

# Brains
from brains.attacker.attacker_brain import AttackerBrain
from brains.defender.defender_brain import DefenderBrain
from brains.time.time_engine import TimeEngine

# Core
from core.intelligence_loop import CoreIntelligenceLoop

# Memory & Evolution
from memory.experience_memory import ExperienceMemory
from evolution.self_mutation import SelfMutationEngine

# Reports
from reports.future_report import FutureReportEngine


def run_full_cycle(verbose=False):
    """
    Runs a full intelligence cycle.
    """

    print("\n[+] Initializing Living Security Intelligence System...\n")

    # Initialize components
    attacker = AttackerBrain()
    defender = DefenderBrain()
    time_engine = TimeEngine()
    memory = ExperienceMemory()
    evolution = SelfMutationEngine()
    reporter = FutureReportEngine()

    # Spawn attacker persona
    attacker.spawn_attacker()

    # Core loop
    core = CoreIntelligenceLoop(attacker, defender, time_engine)

    # Simulated environment (SAFE)
    environment = {
        "exposed_services": ["RDP", "VPN"],
        "user_risk_score": 81,
        "business_impact": "high",
        "alert_noise": 63,
        "threat_intel_match": False
    }

    print("[*] Running intelligence cycle...\n")
    intelligence = core.run_cycle(environment)

    # Experience Memory (learning from decision)
    final_decision = intelligence["defender_view"]["action"]
    if final_decision == "ignore":
        memory.record_experience(
            category="near-miss",
            trigger="weak credential signal",
            decision="ignored early signal",
            outcome="attacker gained persistence",
            lesson="Early identity signals must be respected",
            severity=7
        )

    # Time analysis
    time_engine.record_event(
        event_type="identity_anomaly",
        severity=6,
        description="Unusual authentication behavior detected"
    )
    time_engine.analyze_temporal_risk()

    # Evolution (if pain exists)
    if memory.pain_index() > 0.3:
        evolution.observe_regret(
            {"reason": "defensive hesitation", "impact": "attacker advantage"}
        )
        evolution.mutate_defender_bias(defender)
        evolution.mutate_attacker_model(attacker)

    # Generate report
    report = reporter.generate_report(
        intelligence_snapshot=intelligence,
        defender_snapshot=defender.memory_snapshot(),
        time_snapshot=time_engine.memory_snapshot(),
        memory_snapshot=memory.memory_snapshot(),
        evolution_snapshot=evolution.memory_snapshot()
    )

    print("\n[✓] FUTURE INTELLIGENCE REPORT GENERATED\n")

    if verbose:
        pprint(report)
    else:
        print(json.dumps(report, indent=2))

    print("\n[✓] SYSTEM STATUS:")
    print("- Cycles completed:", core.memory_snapshot()["cycles_completed"])
    print("- Pain index:", memory.pain_index())
    print("- Evolution pressure:", evolution.memory_snapshot()["evolution_pressure"])
    print("\n[✓] Intelligence loop complete.\n")


def main():
    parser = argparse.ArgumentParser(
        description="Living Security Intelligence Organism CLI"
    )

    parser.add_argument(
        "--run",
        action="store_true",
        help="Run a full intelligence cycle"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show full detailed output"
    )

    args = parser.parse_args()

    if args.run:
        run_full_cycle(verbose=args.verbose)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()