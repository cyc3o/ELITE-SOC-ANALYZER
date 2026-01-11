# =====================================================
# ELITE SOC ANALYZER — MITRE ATT&CK FRAMEWORK
# AUTHOR: VISHAL - SOC ENGINEERING
# =====================================================

MITRE_ATTACK = {
    "SSH_BRUTE_FORCE": {
        "TACTIC": "CREDENTIAL ACCESS",
        "TECHNIQUE": "T1110.001",
        "TECHNIQUE_NAME": "PASSWORD GUESSING",
        "DESCRIPTION": "Brute-force password guessing against SSH",
        "DETECTION": "Multiple failed authentication attempts",
        "MITIGATION": "MFA, account lockout, rate limiting"
    },
    "PORT_SCANNING_ACTIVITY": {
        "TACTIC": "DISCOVERY",
        "TECHNIQUE": "T1046",
        "TECHNIQUE_NAME": "NETWORK SERVICE DISCOVERY",
        "DESCRIPTION": "Scanning ports to discover services",
        "DETECTION": "Rapid connection attempts across ports",
        "MITIGATION": "Firewall rules, IDS/IPS"
    },
    "AUTH_FROM_HIGH_RISK_GEO": {
        "TACTIC": "INITIAL ACCESS",
        "TECHNIQUE": "T1078",
        "TECHNIQUE_NAME": "VALID ACCOUNTS",
        "DESCRIPTION": "Login attempts from high-risk countries",
        "DETECTION": "GeoIP correlation on auth logs",
        "MITIGATION": "Geo-fencing, conditional access"
    },
    "KNOWN_THREAT_ACTOR": {
        "TACTIC": "COMMAND AND CONTROL",
        "TECHNIQUE": "T1071",
        "TECHNIQUE_NAME": "APPLICATION LAYER PROTOCOL",
        "DESCRIPTION": "Communication with known malicious infrastructure",
        "DETECTION": "Threat intel IP/domain matching",
        "MITIGATION": "Block at perimeter, threat intel updates"
    },
    "PASSWORD_SPRAYING": {
        "TACTIC": "CREDENTIAL ACCESS",
        "TECHNIQUE": "T1110.003",
        "TECHNIQUE_NAME": "PASSWORD SPRAYING",
        "DESCRIPTION": "Same password attempted across many users",
        "DETECTION": "Single IP targeting multiple accounts",
        "MITIGATION": "Rate limiting, MFA"
    },
    "ACCOUNT_COMPROMISE": {
        "TACTIC": "LATERAL MOVEMENT",
        "TECHNIQUE": "T1078.003",
        "TECHNIQUE_NAME": "LOCAL ACCOUNTS",
        "DESCRIPTION": "Single account used from many IPs",
        "DETECTION": "User behavior anomaly detection",
        "MITIGATION": "Password reset, session monitoring"
    }
}