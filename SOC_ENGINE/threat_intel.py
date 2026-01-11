# =====================================================
# ELITE SOC ANALYZER v4.0 — THREAT INTELLIGENCE ENGINE
# AUTHOR: VISHAL - SOC ENGINEERING
# =====================================================

from datetime import datetime, timedelta
from config import (
    ENABLE_LIVE_THREAT_INTEL,
    ABUSEIPDB_API_KEY,
    VIRUSTOTAL_API_KEY
)
from ui import display_warning

# ==================== LIVE THREAT INTEL ====================

class LiveThreatIntel:
    """
    LIVE THREAT INTELLIGENCE (ABUSEIPDB / VIRUSTOTAL)
    """

    def __init__(self):
        self.cache = {}
        self.cache_expiry = timedelta(hours=24)

    def check_abuseipdb(self, ip):
        if not ENABLE_LIVE_THREAT_INTEL:
            return None

        cache_key = f"ABUSE_{ip}"
        if cache_key in self.cache:
            data, ts = self.cache[cache_key]
            if datetime.now() - ts < self.cache_expiry:
                return data

        try:
            import requests
            url = "https://api.abuseipdb.com/api/v2/check"
            headers = {
                "Key": ABUSEIPDB_API_KEY,
                "Accept": "application/json"
            }
            params = {
                "ipAddress": ip,
                "maxAgeInDays": 90
            }

            r = requests.get(url, headers=headers, params=params, timeout=10)
            if r.status_code == 200:
                data = r.json().get("data", {})
                result = {
                    "CONFIDENCE_SCORE": data.get("abuseConfidenceScore", 0),
                    "TOTAL_REPORTS": data.get("totalReports", 0),
                    "COUNTRY": data.get("countryCode", "UNK")
                }
                self.cache[cache_key] = (result, datetime.now())
                return result
        except Exception as e:
            display_warning(f"ABUSEIPDB ERROR: {e}")

        return None

    def check_virustotal(self, ip):
        if not ENABLE_LIVE_THREAT_INTEL:
            return None

        cache_key = f"VT_{ip}"
        if cache_key in self.cache:
            data, ts = self.cache[cache_key]
            if datetime.now() - ts < self.cache_expiry:
                return data

        try:
            import requests
            url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
            headers = {"x-apikey": VIRUSTOTAL_API_KEY}

            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                stats = r.json()["data"]["attributes"]["last_analysis_stats"]
                result = {
                    "MALICIOUS": stats.get("malicious", 0),
                    "SUSPICIOUS": stats.get("suspicious", 0)
                }
                self.cache[cache_key] = (result, datetime.now())
                return result
        except Exception as e:
            display_warning(f"VIRUSTOTAL ERROR: {e}")

        return None


# ==================== STATIC + LIVE THREAT ENGINE ====================

class ThreatIntelligence:
    """
    COMBINED STATIC & LIVE THREAT INTELLIGENCE
    """

    def __init__(self):
        self.malicious_ips = set()
        self.tor_exit_nodes = set()
        self.live = LiveThreatIntel()
        self._load_static_feeds()

    def _load_static_feeds(self):
        self.malicious_ips.update([
            "185.210.45.22", "94.102.61.24", "45.155.205.233",
            "91.240.118.123", "198.98.51.189", "104.244.74.55"
        ])

        self.tor_exit_nodes.update([
            "185.220.100.254", "185.220.101.4", "185.220.101.8"
        ])

    def check_ip_reputation(self, ip):
        threats = []
        live_data = {}

        if ip in self.malicious_ips:
            threats.append("KNOWN_MALICIOUS_IP")

        if ip in self.tor_exit_nodes:
            threats.append("TOR_EXIT_NODE")

        if ENABLE_LIVE_THREAT_INTEL:
            abuse = self.live.check_abuseipdb(ip)
            if abuse and abuse["CONFIDENCE_SCORE"] >= 70:
                threats.append("LIVE_ABUSEIPDB_MATCH")
                live_data["ABUSEIPDB"] = abuse

            vt = self.live.check_virustotal(ip)
            if vt and vt["MALICIOUS"] >= 3:
                threats.append("LIVE_VIRUSTOTAL_MATCH")
                live_data["VIRUSTOTAL"] = vt

        return threats, live_data

    def get_geoip_info(self, ip):
        geo_db = {
            "185.210.45.22": {"COUNTRY": "RU", "CITY": "MOSCOW"},
            "45.155.205.233": {"COUNTRY": "IR", "CITY": "TEHRAN"},
            "8.8.8.8": {"COUNTRY": "US", "CITY": "MOUNTAIN VIEW"}
        }

        return geo_db.get(ip, {
            "COUNTRY": "UNKNOWN",
            "CITY": "UNKNOWN"
        })