# =====================================================
# ELITE SOC ANALYZER v7.5 — MASTER SOC ORCHESTRATOR
# AUTHOR: VISHAL — SOC ENGINEERING (L5 / ARCHITECT)
# =====================================================

import os
import sys
import traceback
from datetime import datetime

# =====================================================
# PATH SAFETY (CRITICAL)
# =====================================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# =====================================================
# UI LAYER
# =====================================================

from ui.ui import (
    display_banner,
    display_status,
    display_warning,
    display_error
)

# =====================================================
# CORE ENGINE (FIXED)
# =====================================================

from core.analysis_engine import AnalysisEngine   # ← FIX: removed unused import

# =====================================================
# COGNITIVE SUBSYSTEMS
# =====================================================

from brains.attacker.attacker_brain import AttackerBrain
from brains.defender.defender_brain import DefenderBrain
from brains.time.time_engine import TimeEngine
from memory.experience_memory import ExperienceMemory
from evolution.self_mutation import SelfMutationEngine
from core.intelligence_loop import CoreIntelligenceLoop

# =====================================================
# REPORTING
# =====================================================

from reports.reports import ReportGenerator
from reports.html_report import HTMLReportGenerator
from reports.mitre_matrix import MitreMatrixGenerator
from reports.siem_export import SIEMExporter
from reports.future_report import FutureReportEngine

# Dashboard
from ui.dashboard_export import export_dashboard_data

# =====================================================
# UTILITIES
# =====================================================

from utils.file_picker import (
    file_picker_logs,
    paste_log_data,
    analyze_any_file,
    cleanup_temp
)

# =====================================================
# SAFE EXECUTION WRAPPER
# =====================================================

def safe_execute(fn, context="operation"):
    try:
        return fn()
    except KeyboardInterrupt:
        display_warning("OPERATION INTERRUPTED BY USER")
        return None
    except Exception:
        display_error(f"SYSTEM ERROR DURING {context.upper()}")
        traceback.print_exc()
        return None


# =====================================================
# SYSTEM INITIALIZATION
# =====================================================

def initialize_soc_system():
    display_status("INITIALIZING SOC SUBSYSTEMS")

    memory = ExperienceMemory()
    defender = DefenderBrain()
    attacker = AttackerBrain()
    time_engine = TimeEngine()
    evolution = SelfMutationEngine()

    engine = AnalysisEngine(
        experience_memory=memory,
        defender_brain=defender,
        time_engine=time_engine,
        mutation_engine=evolution
    )

    reporting = {
        "reporter": ReportGenerator(),
        "html": HTMLReportGenerator(),
        "siem": SIEMExporter(),
        "future": FutureReportEngine()
    }

    return engine, memory, defender, attacker, time_engine, evolution, reporting


# =====================================================
# CLASSIC SOC PIPELINE
# =====================================================

def run_classic_analysis(engine, reporting, path, temp_file=None):
    alerts = engine.analyze_file(path)

    if not alerts:
        display_warning("NO ALERTS GENERATED")
        return

    export_dashboard_data(alerts, engine.stats)

    report_id = reporting["reporter"].generate_reports(alerts, engine.stats)
    reporting["html"].generate_html(alerts, engine.stats, report_id)
    MitreMatrixGenerator.generate(alerts, report_id)
    reporting["siem"].export(alerts, report_id)

    if temp_file:
        cleanup_temp(temp_file)

    display_status("SOC ANALYSIS COMPLETE")
    display_status("REPORTS + DASHBOARD UPDATED")


# =====================================================
# COGNITIVE SIMULATION
# =====================================================

def run_cognitive_simulation(
    attacker,
    defender,
    time_engine,
    memory,
    evolution,
    reporting
):
    display_status("STARTING COGNITIVE INTELLIGENCE SIMULATION")

    attacker.spawn_attacker()

    core = CoreIntelligenceLoop(
        attacker_brain=attacker,
        defender_brain=defender,
        time_engine=time_engine
    )

    intelligence = core.run_cycle({
        "exposed_services": ["RDP", "VPN", "SSH"],
        "user_risk_score": 82,
        "business_impact": "high",
        "alert_noise": 64,
        "threat_intel_match": False
    })

    time_engine.record_event(
        event_type="identity_anomaly",
        severity=6,
        description="Anomalous authentication behavior detected"
    )

    time_engine.analyze_temporal_risk()

    if intelligence["defender_view"]["action"] == "ignore":
        memory.record_experience(
            category="near-miss",
            trigger="weak credential signal",
            decision="ignored alert",
            outcome="attacker persistence",
            lesson="Early identity signals must not be ignored",
            severity=7
        )

    if memory.pain_index() > 0.3:
        evolution.observe_regret(
            {"cause": "defensive hesitation", "impact": "attacker advantage"}
        )
        evolution.mutate_defender_bias(defender)
        evolution.mutate_attacker_model(attacker)

    future = reporting["future"].generate_report(
        intelligence_snapshot=intelligence,
        defender_snapshot=defender.memory_snapshot(),
        time_snapshot=time_engine.memory_snapshot(),
        memory_snapshot=memory.memory_snapshot(),
        evolution_snapshot=evolution.memory_snapshot()
    )

    print("\n📘 FUTURE INTELLIGENCE REPORT\n")
    print(future)
    input("\nPRESS ENTER TO RETURN TO MENU...")


# =====================================================
# MAIN MENU
# =====================================================

def main_menu():
    display_banner()

    while True:
        print("\n🧠 ELITE SOC ANALYZER — INDUSTRY OPERATIONS")
        print("================================================")
        print("1 - 📄 ANALYZE LOG FILE")
        print("2 - 📁 LOG FILE PICKER")
        print("3 - 📋 PASTE LOG DATA")
        print("4 - 🔍 ANALYZE ANY FILE")
        print("5 - 🚀 RUN COGNITIVE SIMULATION")
        print("6 - ❌ EXIT")
        print("================================================")

        choice = input("ENTER CHOICE (1-6): ").strip()

        if choice == "6":
            display_status("SECURE SHUTDOWN — SOC SYSTEM HALTED")
            sys.exit(0)

        engine, memory, defender, attacker, time_engine, evolution, reporting = (
            initialize_soc_system()
        )

        temp_file = None

        if choice == "1":
            path = input("ENTER LOG FILE PATH: ").strip()
            if not os.path.isfile(path):
                display_error("INVALID FILE PATH")
                continue
            safe_execute(lambda: run_classic_analysis(engine, reporting, path), "log analysis")

        elif choice == "2":
            path = file_picker_logs()
            if path:
                safe_execute(lambda: run_classic_analysis(engine, reporting, path), "file picker")

        elif choice == "3":
            temp_file = paste_log_data()
            if temp_file:
                safe_execute(
                    lambda: run_classic_analysis(engine, reporting, temp_file, temp_file),
                    "paste analysis"
                )

        elif choice == "4":
            temp_file = analyze_any_file()
            if temp_file:
                safe_execute(
                    lambda: run_classic_analysis(engine, reporting, temp_file, temp_file),
                    "generic analysis"
                )

        elif choice == "5":
            safe_execute(
                lambda: run_cognitive_simulation(
                    attacker, defender, time_engine, memory, evolution, reporting
                ),
                "cognitive simulation"
            )
        else:
            display_warning("INVALID OPTION")


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    main_menu()
