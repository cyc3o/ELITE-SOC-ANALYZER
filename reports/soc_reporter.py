import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import json
from datetime import datetime
from config import TOOL_NAME, TOOL_VERSION


def generate_report(correlated_incidents, output_dir):
    report = {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "generated_at": datetime.utcnow().isoformat(),
        "total_incidents": len(correlated_incidents),
        "incidents": correlated_incidents
    }

    os.makedirs(output_dir, exist_ok=True)

    with open(f"{output_dir}/soc_report.json", "w") as f:
        json.dump(report, f, indent=4)