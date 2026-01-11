# =====================================================
# ELITE SOC ANALYZER v4.0 — RISK SCORING ENGINE
# AUTHOR: VISHAL - SOC ENGINEERING
# =====================================================

from config import (
    WEIGHT_FAILED_AUTH,
    WEIGHT_PORT_SCAN,
    WEIGHT_GEO_RISK,
    WEIGHT_THREAT_INTEL,
    WEIGHT_TOR_EXIT
)

# ==================== ENTERPRISE RISK SCORING ====================

def calculate_risk_score(
    failed_attempts=0,
    port_scans=0,
    geo_risk=False,
    threat_intel=False,
    tor_exit=False,
    successful_after_failed=False,
    unique_users=0,
    time_window_events=0,
    ml_anomaly_score=0
):
    """
    ENTERPRISE RISK SCORING ALGORITHM
    COMBINES MULTIPLE THREAT INDICATORS WITH WEIGHTED SCORING
    """

    score = 0

    # FAILED AUTHENTICATION ATTEMPTS
    score += failed_attempts * WEIGHT_FAILED_AUTH

    # PORT SCANNING ACTIVITY
    score += port_scans * WEIGHT_PORT_SCAN

    # GEOGRAPHIC RISK
    if geo_risk:
        score += WEIGHT_GEO_RISK

    # THREAT INTELLIGENCE MATCH
    if threat_intel:
        score += WEIGHT_THREAT_INTEL

    # TOR EXIT NODE
    if tor_exit:
        score += WEIGHT_TOR_EXIT

    # SUCCESSFUL LOGIN AFTER FAILURES (COMPROMISE INDICATOR)
    if successful_after_failed:
        score += 15

    # MULTI-USER ATTACK PATTERN (PASSWORD SPRAYING)
    if unique_users >= 3:
        score += 10 + (unique_users * 2)

    # TIME-BASED CORRELATION (RAPID ATTACKS)
    if time_window_events > 20:
        score += 20

    # ML ANOMALY CONTRIBUTION
    score += ml_anomaly_score * 30

    # CAP SCORE AT 100
    return min(int(score), 100)


def calculate_confidence_level(
    data_quality=1.0,
    threat_intel_match=False,
    behavioral_consistency=1.0,
    false_positive_indicators=0
):
    """
    CONFIDENCE LEVEL CALCULATION
    DETERMINES HOW CONFIDENT THE DETECTION IS
    """

    confidence = 50  # BASE CONFIDENCE

    # DATA QUALITY (LOG COMPLETENESS)
    confidence += (data_quality * 20)

    # THREAT INTELLIGENCE CORRELATION
    if threat_intel_match:
        confidence += 25

    # BEHAVIORAL CONSISTENCY
    confidence += (behavioral_consistency * 20)

    # REDUCE CONFIDENCE FOR FP SIGNALS
    confidence -= (false_positive_indicators * 10)

    return max(10, min(int(confidence), 100))