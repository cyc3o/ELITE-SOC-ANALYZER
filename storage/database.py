# =====================================================
# ELITE SOC — INCIDENT DATABASE LAYER
# AUTHOR: VISHAL — SOC ENGINEERING
# =====================================================

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict

DB_PATH = "soc.db"


# ==================== CONNECTION ====================

def _connect():
    """
    Create SQLite connection with safe settings
    """
    return sqlite3.connect(
        DB_PATH,
        detect_types=sqlite3.PARSE_DECLTYPES,
        check_same_thread=False
    )


# ==================== INITIALIZATION ====================

def init_db():
    """
    Initialize SOC incident database
    """
    conn = _connect()
    cur = conn.cursor()

    # INCIDENT TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        alert_id TEXT PRIMARY KEY,
        threat_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        source TEXT,
        incident_state TEXT DEFAULT 'OPEN',
        confidence INTEGER,
        risk_score INTEGER,
        feedback TEXT,
        first_seen TEXT,
        last_seen TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    # INDEXES FOR FAST SOC QUERIES
    cur.execute("CREATE INDEX IF NOT EXISTS idx_state ON incidents (incident_state)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_severity ON incidents (severity)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_threat ON incidents (threat_type)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_updated ON incidents (updated_at)")

    conn.commit()
    conn.close()


# ==================== UPSERT INCIDENT ====================

def upsert_incident(alert: Dict):
    """
    Insert or update an incident from alert object
    """
    conn = _connect()
    cur = conn.cursor()

    now = datetime.utcnow().isoformat()

    cur.execute("""
    INSERT INTO incidents (
        alert_id, threat_type, severity, source,
        incident_state, confidence, risk_score,
        feedback, first_seen, last_seen,
        created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(alert_id) DO UPDATE SET
        incident_state = excluded.incident_state,
        confidence     = excluded.confidence,
        risk_score     = excluded.risk_score,
        feedback       = excluded.feedback,
        last_seen      = excluded.last_seen,
        updated_at     = excluded.updated_at
    """, (
        alert.get("ALERT_ID"),
        alert.get("THREAT_TYPE"),
        alert.get("THREAT_LEVEL"),
        alert.get("SOURCE_IP") or alert.get("USERNAME"),
        alert.get("INCIDENT_STATE", "OPEN"),
        alert.get("CONFIDENCE"),
        alert.get("RISK_SCORE"),
        alert.get("FEEDBACK"),
        alert.get("FIRST_SEEN"),
        alert.get("LAST_SEEN"),
        now,
        now
    ))

    conn.commit()
    conn.close()


# ==================== UPDATE INCIDENT STATE ====================

def update_incident_state(
    alert_id: str,
    state: str,
    feedback: Optional[str] = None
):
    """
    Update incident lifecycle state (OPEN / ACK / CLOSED)
    """
    conn = _connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE incidents
    SET incident_state = ?,
        feedback = ?,
        updated_at = ?
    WHERE alert_id = ?
    """, (
        state,
        feedback,
        datetime.utcnow().isoformat(),
        alert_id
    ))

    conn.commit()
    conn.close()


# ==================== FETCH INCIDENTS ====================

def get_incidents(
    state: Optional[str] = None,
    severity: Optional[str] = None
) -> List[Dict]:
    """
    Fetch incidents with optional filters
    """
    conn = _connect()
    cur = conn.cursor()

    query = "SELECT * FROM incidents WHERE 1=1"
    params = []

    if state:
        query += " AND incident_state = ?"
        params.append(state)

    if severity:
        query += " AND severity = ?"
        params.append(severity)

    query += " ORDER BY updated_at DESC"

    cur.execute(query, params)
    rows = cur.fetchall()
    columns = [d[0] for d in cur.description]

    conn.close()

    return [dict(zip(columns, r)) for r in rows]


# ==================== METRICS (SOC KPIs) ====================

def get_metrics() -> Dict:
    """
    SOC metrics: open incidents, closed, MTTR base
    """
    conn = _connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM incidents WHERE incident_state='OPEN'")
    open_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM incidents WHERE incident_state='CLOSED'")
    closed_count = cur.fetchone()[0]

    conn.close()

    return {
        "OPEN_INCIDENTS": open_count,
        "CLOSED_INCIDENTS": closed_count
    }