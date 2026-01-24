# =====================================================
# ELITE SOC ANALYZER v4.0 — ML ANOMALY DETECTION ENGINE
# AUTHOR: VISHAL - SOC ENGINEERING
# =====================================================

from collections import defaultdict, Counter
from datetime import datetime

from config import ENABLE_ML_ANOMALY_DETECTION
from ui.ui import display_status

# ==================== ML ANOMALY DETECTOR ====================

class MLAnomalyDetector:
    """
    SIMPLE BUT EFFECTIVE ML-STYLE ANOMALY DETECTION
    BASED ON STATISTICAL AND BEHAVIORAL BASELINES
    """

    def __init__(self):
        self.baselines = {}
        self.historical_patterns = defaultdict(list)

    # ==================== BASELINE BUILDING ====================

    def build_baseline(self, events):
        """
        BUILD BEHAVIORAL BASELINE FROM HISTORICAL EVENTS
        """

        if not ENABLE_ML_ANOMALY_DETECTION:
            return

        display_status("BUILDING ML BEHAVIORAL BASELINE")

        # IP FREQUENCY BASELINE
        ip_counts = Counter(
            e.get("ip") for e in events if e.get("ip")
        )
        self.baselines["ip_frequency_mean"] = (
            sum(ip_counts.values()) / max(len(ip_counts), 1)
        )

        # USER FREQUENCY BASELINE
        user_counts = Counter(
            e.get("user") for e in events if e.get("user")
        )
        self.baselines["user_frequency_mean"] = (
            sum(user_counts.values()) / max(len(user_counts), 1)
        )

        # EVENT TYPE DISTRIBUTION BASELINE
        event_types = Counter(
            e.get("EVENT_TYPE") for e in events if e.get("EVENT_TYPE")
        )
        total_events = len(events)

        self.baselines["event_distribution"] = {
            k: v / total_events
            for k, v in event_types.items()
            if total_events > 0
        }

    # ==================== ANOMALY DETECTION ====================

    def detect_anomalies(self, ip, events):
        """
        DETECT ANOMALOUS BEHAVIOR FOR A GIVEN IP
        RETURNS A SCORE BETWEEN 0.0 AND 1.0
        """

        if not ENABLE_ML_ANOMALY_DETECTION or not self.baselines:
            return 0.0

        anomaly_score = 0.0
        indicators = 0

        # ==================== FREQUENCY ANOMALY ====================

        event_count = len(events)
        expected_freq = self.baselines.get("ip_frequency_mean", 5)

        if event_count > (expected_freq * 3):
            anomaly_score += 0.3
            indicators += 1

        # ==================== EVENT DISTRIBUTION ANOMALY ====================

        event_types = Counter(
            e.get("EVENT_TYPE") for e in events if e.get("EVENT_TYPE")
        )

        for event_type, count in event_types.items():
            expected_ratio = (
                self.baselines
                .get("event_distribution", {})
                .get(event_type, 0.1)
            )
            actual_ratio = count / max(len(events), 1)

            if actual_ratio > (expected_ratio * 4):
                anomaly_score += 0.2
                indicators += 1

        # ==================== TIME-BASED ANOMALY ====================

        if len(events) >= 3:
            timestamps = [
                datetime.fromisoformat(e["INGEST_TIME"])
                for e in events
                if "INGEST_TIME" in e
            ]

            if len(timestamps) >= 2:
                time_diffs = [
                    (timestamps[i + 1] - timestamps[i]).total_seconds()
                    for i in range(len(timestamps) - 1)
                ]

                avg_diff = sum(time_diffs) / max(len(time_diffs), 1)

                # VERY RAPID ACTIVITY
                if avg_diff < 5:
                    anomaly_score += 0.3
                    indicators += 1

        # ==================== NORMALIZATION ====================

        if indicators > 0:
            anomaly_score = min(anomaly_score, 1.0)

        return anomaly_score