# =====================================================
# ELITE SOC ANALYZER v5.0 — MAIN ENTRY POINT (SOC L5)
# AUTHOR: VISHAL - SOC ENGINEERING
# =====================================================

import os

from ui import (
    display_banner,
    display_status,
    display_warning,
    display_error
)

from analysis_engine import AnalysisEngine
from reports import ReportGenerator
from html_report import HTMLReportGenerator
from mitre_matrix import MitreMatrixGenerator
from siem_export import SIEMExporter   # 🔥 SOC L5 ADDITION

from file_picker import (
    file_picker_logs,
    paste_log_data,
    analyze_any_file,
    cleanup_temp
)

# ==================== MAIN MENU ====================

def main_menu():
    display_banner()

    while True:
        print("\n🎯 ELITE SOC ANALYZER — OPERATIONS MENU")
        print("======================================")
        print("1 - 📄 ANALYZE LOG FILE")
        print("2 - 📁 LOG FILE PICKER")
        print("3 - 📋 PASTE LOG DATA")
        print("4 - 🔍 ANALYZE ANY FILE")
        print("5 - ❌ EXIT")
        print("======================================")

        choice = input("ENTER CHOICE (1-5): ").strip()

        if choice == "5":
            display_status("SECURE SHUTDOWN COMPLETE")
            break

        engine = AnalysisEngine()
        reporter = ReportGenerator()
        html = HTMLReportGenerator()
        siem = SIEMExporter()  # 🔥 SOC L5

        alerts = None
        temp_file = None

        # ==================== OPTION 1 ====================

        if choice == "1":
            path = input("ENTER LOG FILE PATH: ").strip()

            if not path:
                display_warning("NO FILE PROVIDED")
                continue

            if not os.path.isfile(path):
                display_error("FILE NOT FOUND")
                continue

            alerts = engine.analyze_file(path)

        # ==================== OPTION 2 ====================

        elif choice == "2":
            path = file_picker_logs()
            if not path:
                continue

            alerts = engine.analyze_file(path)

        # ==================== OPTION 3 ====================

        elif choice == "3":
            temp_file = paste_log_data()
            if not temp_file:
                continue

            alerts = engine.analyze_file(temp_file)

        # ==================== OPTION 4 ====================

        elif choice == "4":
            temp_file = analyze_any_file()
            if not temp_file:
                continue

            alerts = engine.analyze_file(temp_file)

        else:
            display_warning("INVALID OPTION")
            continue

        # ==================== REPORTING ====================

        if not alerts:
            display_warning("NO ALERTS GENERATED")
            continue

        report_id = reporter.generate_reports(alerts, engine.stats)

        # Enterprise outputs
        html.generate_html(alerts, engine.stats, report_id)
        MitreMatrixGenerator.generate(alerts, report_id)

        # 🔥 SOC L5 SIEM OUTPUT
        siem.export(alerts, report_id)

        # ==================== CLEANUP ====================

        if temp_file:
            cleanup_temp(temp_file)

        print("\n✅ ANALYSIS COMPLETE (SOC L5)")
        print("📤 SIEM EXPORT READY (NDJSON)")
        input("PRESS ENTER TO RETURN TO MENU...")

# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    main_menu()