# =====================================================
# ELITE SOC ANALYZER v4.0 — LOG PARSER ENGINE
# AUTHOR: VISHAL - SOC ENGINEERING
# =====================================================

import re
import hashlib
from datetime import datetime

# ==================== LOG PARSER ====================

class LogParser:
    """
    ENTERPRISE LOG PARSER WITH PATTERN MATCHING
    SUPPORTS AUTH, FIREWALL, WEB, AND ATTACK LOGS
    """

    def __init__(self):
        # SYSLOG FORMAT
        self.syslog_pattern = re.compile(
            r'(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+)\s+'
            r'(?P<host>\S+)\s+'
            r'(?P<process>[a-zA-Z0-9_\-/]+)'
            r'(?:\[(?P<pid>\d+)\])?:\s+'
            r'(?P<message>.*)'
        )

        # DETECTION PATTERNS
        self.patterns = {
            "SSH_FAILED_PASSWORD": re.compile(
                r'Failed password for (?:invalid user )?(?P<user>\S+) '
                r'from (?P<ip>[0-9.]+)'
            ),
            "SSH_ACCEPTED_PASSWORD": re.compile(
                r'Accepted password for (?P<user>\S+) '
                r'from (?P<ip>[0-9.]+)'
            ),
            "SSH_INVALID_USER": re.compile(
                r'Invalid user (?P<user>\S+) '
                r'from (?P<ip>[0-9.]+)'
            ),
            "AUTH_FAILURE": re.compile(
                r'authentication failure.*rhost=(?P<ip>\S+)'
            ),
            "FIREWALL_BLOCK": re.compile(
                r'BLOCK.*SRC=(?P<ip>[0-9.]+)'
            ),
            "PORT_SCAN": re.compile(
                r'Port scan detected from (?P<ip>[0-9.]+)',
                re.IGNORECASE
            ),
            "CONNECTION_ATTEMPT": re.compile(
                r'SRC=(?P<ip>[0-9.]+).*DPT=(?P<port>\d+)'
            ),
            "SQL_INJECTION": re.compile(
                r'(?i)(sql.*injection|union\s+select).*from (?P<ip>[0-9.]+)'
            ),
            "XSS_ATTACK": re.compile(
                r'(?i)(<script>|xss).*from (?P<ip>[0-9.]+)'
            ),
            "WEB_LOGIN_FAILURE": re.compile(
                r'(?i)(login|wp-login|admin).*failed.*from (?P<ip>[0-9.]+)'
            ),
            "BRUTE_FORCE": re.compile(
                r'(?i)brute.*force.*from (?P<ip>[0-9.]+)'
            ),
            "DOS_ATTACK": re.compile(
                r'(?i)(dos|ddos).*attack.*from (?P<ip>[0-9.]+)'
            )
        }

    # ==================== PARSE LINE ====================

    def parse_line(self, line):
        if not line:
            return None

        raw = line.strip()

        event = {
            "RAW_LINE": raw,
            "INGEST_TIME": datetime.now().isoformat(),
            "LINE_HASH": hashlib.md5(raw.encode()).hexdigest()[:10]
        }

        syslog_match = self.syslog_pattern.match(raw)
        if syslog_match:
            event.update(syslog_match.groupdict())
            message = syslog_match.group("message")
        else:
            message = raw

        for event_type, pattern in self.patterns.items():
            match = pattern.search(message)
            if match:
                event["EVENT_TYPE"] = event_type
                event.update(match.groupdict())
                return event

        if syslog_match:
            event["EVENT_TYPE"] = "SYSLOG_GENERIC"
            return event

        return None