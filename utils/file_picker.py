# =====================================================
# ELITE SOC ANALYZER — SMART FILE PICKER (ANDROID)
# AUTHOR: VISHAL - SOC ENGINEERING
# =====================================================

import os
import time
from ui.ui import display_status, display_warning, display_error
from ui.colors import Colors

# ==================== ROOT DETECTION ====================

def get_default_root():
    """
    ANDROID-FIRST ROOT DIRECTORY DETECTION
    """
    if os.path.isdir("/storage/emulated/0"):
        return "/storage/emulated/0"
    return os.getcwd()

# ==================== SMART SEARCH ====================

def smart_file_search(filename, base_dir=None, max_depth=4):
    """
    SEARCH FILE BY NAME WITH DEPTH LIMIT
    """
    if base_dir is None:
        base_dir = get_default_root()

    matches = []

    for root, dirs, files in os.walk(base_dir):
        depth = root[len(base_dir):].count(os.sep)
        if depth > max_depth:
            dirs[:] = []
            continue

        for f in files:
            if f.lower() == filename.lower():
                matches.append(os.path.join(root, f))

    return matches

# ==================== LOG FILE PICKER ====================

def file_picker_logs(base_dir=None, max_depth=3):
    """
    INTERACTIVE LOG FILE PICKER FOR ANDROID
    """
    if base_dir is None:
        base_dir = get_default_root()

    log_files = []

    for root, dirs, files in os.walk(base_dir):
        depth = root[len(base_dir):].count(os.sep)
        if depth > max_depth:
            dirs[:] = []
            continue

        for f in files:
            if f.lower().endswith(".log"):
                log_files.append(os.path.join(root, f))

    if not log_files:
        display_warning("NO LOG FILES FOUND")
        return None

    print("\n📁 LOG FILE PICKER\n")
    for i, path in enumerate(log_files, 1):
        size_kb = os.path.getsize(path) // 1024
        short = path.replace(base_dir + os.sep, "")
        print(f"[{i}] {short} ({size_kb} KB)")

    print("[0] CANCEL")

    choice = input(f"{Colors.CYAN}> {Colors.RESET}").strip()

    if not choice.isdigit():
        return None

    choice = int(choice)
    if choice == 0:
        return None

    if 1 <= choice <= len(log_files):
        return log_files[choice - 1]

    display_warning("INVALID SELECTION")
    return None

# ==================== PASTE LOG DATA ====================

def paste_log_data():
    """
    ALLOW USER TO PASTE RAW LOG DATA
    """
    print("\n📋 PASTE LOG DATA — TYPE 'END' TO FINISH\n")

    lines = []
    while True:
        try:
            line = input()
        except KeyboardInterrupt:
            break

        if line.strip() == "END":
            break
        lines.append(line)

    if not lines:
        display_warning("NO LOG DATA PROVIDED")
        return None

    temp = f"._SOC_TEMP_{int(time.time())}.log"
    with open(temp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    display_status(f"TEMP LOG CREATED: {temp}")
    return temp

# ==================== ANALYZE ANY FILE ====================

def analyze_any_file():
    """
    ANALYZE ANY FILE TYPE USING SMART SEARCH
    """
    name = input(f"{Colors.CYAN}ENTER FILE NAME OR PATH: {Colors.RESET}").strip()

    if not name:
        display_warning("NO INPUT PROVIDED")
        return None

    if os.path.isfile(name):
        resolved = name
    else:
        alt = os.path.join(get_default_root(), name)
        if os.path.isfile(alt):
            resolved = alt
        else:
            matches = smart_file_search(os.path.basename(name))
            if not matches:
                display_error("NO MATCHING FILES FOUND")
                return None

            print("\n🔍 MATCHING FILES:\n")
            root = get_default_root()
            for i, path in enumerate(matches, 1):
                short = path.replace(root + os.sep, "")
                print(f"[{i}] {short}")

            print("[0] CANCEL")
            choice = input(f"{Colors.CYAN}> {Colors.RESET}").strip()

            if not choice.isdigit():
                return None

            choice = int(choice)
            if choice == 0:
                return None

            if 1 <= choice <= len(matches):
                resolved = matches[choice - 1]
            else:
                display_warning("INVALID SELECTION")
                return None

    try:
        with open(resolved, "r", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        display_error(f"FAILED TO READ FILE: {e}")
        return None

    if not content.strip():
        display_warning("FILE EMPTY OR UNREADABLE")
        return None

    temp = f"._SOC_TEMP_ANY_{int(time.time())}.log"
    with open(temp, "w", encoding="utf-8") as f:
        f.write(content)

    display_status(f"FILE LOADED: {resolved}")
    return temp

# ==================== CLEANUP ====================

def cleanup_temp(path):
    try:
        if path and path.startswith("._SOC_TEMP_") and os.path.isfile(path):
            os.remove(path)
    except:
        pass