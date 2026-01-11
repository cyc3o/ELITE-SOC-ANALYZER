# =====================================================
# ELITE SOC ANALYZER — HACKER DINOSAUR UI
# AUTHOR: VISHAL - SOC ENGINEERING
# =====================================================

import sys
from colors import Colors

# ==================== BANNER ====================

def display_banner():
    print(Colors.RED + r"""
◣　　　　　　◢
█◣　　　　◢█
████████
█　▎██　▎█            
███◥◤███             @GitHub - cyc3o
████████                         
◥██████◤
　　◢██◣　　　◢
　　████　◢█◤
　　████　█
　　████　█          
　　████◢◤
　██████  
""" + Colors.RESET)

    print(
        Colors.RED
        + " [ ELITE SOC ANALYZER — ANALYZER MODE ACTIVATED ] "
        + Colors.RESET
    )
    print(Colors.RED + "═" * 55 + Colors.RESET)


# ==================== BASIC OUTPUT ====================

def display_status(msg):
    print(f"{Colors.GREEN}[+] {msg}{Colors.RESET}")

def display_warning(msg):
    print(f"{Colors.YELLOW}[!] {msg}{Colors.RESET}")

def display_error(msg):
    print(f"{Colors.RED}[-] {msg}{Colors.RESET}")


# ==================== SEVERITY COLORS ====================

def severity_color(level):
    return {
        "CRITICAL": Colors.RED,
        "HIGH": Colors.MAGENTA,
        "MEDIUM": Colors.YELLOW,
        "LOW": Colors.GREEN,
        "INFO": Colors.CYAN
    }.get(level.upper(), Colors.WHITE)


# ==================== ALERT PRINT ====================

def print_alert(alert):
    level = alert.get("THREAT_LEVEL", "INFO")
    color = severity_color(level)

    print(
        color
        + f"[{level}] {alert.get('THREAT_TYPE','UNKNOWN')} "
        + f"→ {alert.get('SOURCE_IP','-')}"
        + Colors.RESET
    )

    mitre = alert.get("MITRE_ATTACK")
    if mitre:
        print(
            Colors.CYAN
            + f"    MITRE: {mitre.get('TACTIC')} / {mitre.get('TECHNIQUE')}"
            + Colors.RESET
        )

    action = alert.get("RECOMMENDED_ACTION")
    if action:
        print(
            Colors.YELLOW
            + f"    ACTION: {action}"
            + Colors.RESET
        )


# ==================== SUMMARY ====================

def display_summary(stats):
    print(Colors.RED + "\n[ SOC SUMMARY ]" + Colors.RESET)
    print(Colors.RED + "────────────────────────────" + Colors.RESET)

    for k, v in stats.items():
        print(f"{k.replace('_',' ').upper():<25}: {v}")

    print(Colors.RED + "────────────────────────────" + Colors.RESET)


# ==================== PROGRESS BAR ====================

def progress_bar(current, total, label=""):
    if total <= 0:
        return

    percent = int((current / total) * 100)
    filled = percent // 4
    bar = "█" * filled + "-" * (25 - filled)

    sys.stdout.write(
        f"\r{Colors.RED}{label} [{bar}] {percent}%{Colors.RESET}"
    )
    sys.stdout.flush()

    if current >= total:
        print()


# ==================== PAUSE ====================

def wait_for_user():
    input(Colors.CYAN + "\n[ PRESS ENTER TO CONTINUE ]" + Colors.RESET)