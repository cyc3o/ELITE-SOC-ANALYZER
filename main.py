# =====================================================
# ELITE SOC ANALYZER - ROOT ENTRY POINT
# VERSION: 4.0
# AUTHOR: VISHAL THAKUR
# =====================================================

import sys
import os

# ADD SOC ENGINE TO PYTHON PATH
SOC_ENGINE_PATH = os.path.join(os.path.dirname(__file__), "SOC ENGINE")
sys.path.insert(0, SOC_ENGINE_PATH)

def main():
    try:
        from main import main as soc_main
        soc_main()
    except ImportError as e:
        print("[ERROR] FAILED TO LOAD SOC ENGINE")
        print(e)
        print("\n[HINT] CHECK FOLDER NAME OR FILE STRUCTURE")

if __name__ == "__main__":
    main()