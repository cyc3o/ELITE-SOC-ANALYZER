# =====================================================
# ELITE SOC ANALYZER — CONNECTED CONFIGURATION
# AUTHOR: VISHAL — SOC ENGINEERING
# BACKWARD + FORWARD COMPATIBLE
# =====================================================

# ==================== TOOL METADATA ====================

TOOL_NAME = "ELITE SOC ANALYZER"
TOOL_VERSION = "6.0-COGNITIVE"
TOOL_AUTHOR = "VISHAL - SOC ENGINEERING"
TOOL_MODE = "PREDICTIVE / SELF-EVOLVING"

# ==================== CORE MODES ====================

ENABLE_COGNITIVE_MODE = True
ENABLE_LEGACY_ANALYSIS = True
ENABLE_FULL_INTELLIGENCE_LOOP = True

# =====================================================
# LOG PATHS (🔥 OLD + NEW BOTH CONNECTED 🔥)
# =====================================================

LOGS_PATH = "./logs/raw/"
PARSED_PATH = "./logs/parsed/"
CORRELATED_PATH = "./logs/correlated/"
REPORTS_PATH = "./reports/"

LOGS_RAW_PATH = LOGS_PATH
LOGS_PARSED_PATH = PARSED_PATH
LOGS_CORRELATED_PATH = CORRELATED_PATH
SOC_REPORT_OUTPUT = "./soc_reports/"

# =====================================================
# DETECTION BASELINES
# =====================================================

FAILED_LOGIN_THRESHOLD = 5
FAILED_LOGIN_WINDOW_MINUTES = 5

PORT_SCAN_THRESHOLD = 15
PORT_SCAN_WINDOW_MINUTES = 10

GENERIC_SUSPICIOUS_THRESHOLD = 10

# ✅ FIX: Account sharing / IP hopping detection
ACCOUNT_IP_THRESHOLD = 3
ACCOUNT_IP_WINDOW_MINUTES = 15

# =====================================================
# RISK SCORING
# =====================================================

WEIGHT_FAILED_AUTH = 6
WEIGHT_PORT_SCAN = 4
WEIGHT_GEO_RISK = 20
WEIGHT_THREAT_INTEL = 30
WEIGHT_TOR_EXIT = 25
WEIGHT_IDENTITY_ANOMALY = 18
WEIGHT_BEHAVIOR_DRIFT = 22

MAX_RISK_SCORE = 100

# =====================================================
# GEO CONTEXT
# =====================================================

ENABLE_GEO_CONTEXT = True

GEO_RISK_COUNTRIES = [
    "RU", "CN", "KP", "IR", "SY",
    "AF", "IQ", "BY", "VE"
]

# =====================================================
# FALSE POSITIVE REDUCTION
# =====================================================

ENABLE_FP_REDUCTION = True
FP_SUCCESSFUL_LOGIN_THRESHOLD = 3
FP_DECAY_WINDOW_HOURS = 24

# =====================================================
# ALERT NOISE CONTROL
# =====================================================

ENABLE_ALERT_DEDUPLICATION = True
ALERT_DEDUP_WINDOW_MINUTES = 60
MAX_ALERT_NOISE_PERCENT = 70

# =====================================================
# THREAT INTELLIGENCE
# =====================================================

ENABLE_LIVE_THREAT_INTEL = False

THREAT_INTEL_SOURCES = {
    "abuseipdb": False,
    "virustotal": False,
    "alienvault": False
}

ABUSEIPDB_API_KEY = "YOUR_API_KEY_HERE"
VIRUSTOTAL_API_KEY = "YOUR_API_KEY_HERE"

# =====================================================
# ML & HEURISTICS
# =====================================================

ENABLE_ML_ANOMALY_DETECTION = True
ANOMALY_THRESHOLD = 0.75
ML_CONFIDENCE_WEIGHT = 0.3

# =====================================================
# TEMPORAL / FUTURE INTELLIGENCE
# =====================================================

ENABLE_TEMPORAL_ANALYSIS = True
TEMPORAL_DECAY_DAYS = 14
BREACH_PROBABILITY_WARNING = 0.6
BREACH_PROBABILITY_CRITICAL = 0.8

# =====================================================
# EXPERIENCE MEMORY
# =====================================================

ENABLE_EXPERIENCE_MEMORY = True
PAIN_SEVERITY_THRESHOLD = 6
MAX_MEMORY_RETENTION = 500

# =====================================================
# SELF EVOLUTION
# =====================================================

ENABLE_SELF_MUTATION = True
EVOLUTION_PRESSURE_THRESHOLD = 0.3
MAX_MUTATION_RATE = 0.2
MATURITY_CAP = 10.0

# =====================================================
# REPORTING & EXPORT
# =====================================================

ENABLE_HTML_REPORT = True
ENABLE_MITRE_MATRIX = True
ENABLE_SIEM_EXPORT = True
ENABLE_FUTURE_REPORT = True

IOC_EXPORT_DIR = "./ioc_feeds/"
SIEM_EXPORT_DIR = "./siem_exports/"

# =====================================================
# SAFETY & GOVERNANCE
# =====================================================

ALLOW_AUTOMATED_CONTAINMENT = False
LOG_ALL_DECISIONS = True
ENABLE_AUDIT_TRAIL = True

# =====================================================
# SYSTEM PHILOSOPHY
# =====================================================

SYSTEM_PHILOSOPHY = (
    "Security is not about certainty. "
    "It is about reducing regret over time."
)

# ==================== BACKWARD COMPATIBILITY ====================

REPORT_DIR = REPORTS_PATH
