import os
import json
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF

# FORCE ABSOLUTE PATHS - This ensures the Scanner and Dashboard match
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CLOUD_DIR = os.path.join(BASE_DIR, "cloud_storage")
QUARANTINE_DIR = os.path.join(BASE_DIR, "quarantine")
LOG_PATH = os.path.join(DATA_DIR, "audit_log.json")
FEED_PATH = os.path.join(DATA_DIR, "live_feed.txt")
LOCKDOWN_FLAG = os.path.join(DATA_DIR, "lockdown.flag")

def ensure_dirs():
    """Create folders if they don't exist, handling Windows file/folder conflicts."""
    for d in [DATA_DIR, CLOUD_DIR, QUARANTINE_DIR]:
        if os.path.exists(d) and not os.path.isdir(d):
            os.remove(d) 
        os.makedirs(d, exist_ok=True)

def load_logs():
    ensure_dirs()
    if not os.path.exists(LOG_PATH) or os.stat(LOG_PATH).st_size == 0:
        return pd.DataFrame(columns=["timestamp", "file", "reason", "status"])
    try:
        return pd.read_json(LOG_PATH)
    except:
        return pd.DataFrame(columns=["timestamp", "file", "reason", "status"])

def save_log_entry(filename, reason):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file": filename, "reason": reason, "status": "QUARANTINED"
    }
    df = load_logs()
    logs = df.to_dict('records')
    logs.append(entry)
    with open(LOG_PATH, 'w') as f:
        json.dump(logs, f, indent=4)
    with open(FEED_PATH, "a") as f:
        f.write(f"[{entry['timestamp'][-8:]}] ALERT: {reason} in {filename}\n")

def get_risk_score():
    df = load_logs()
    if df.empty: return 0
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    one_min_ago = datetime.now() - timedelta(seconds=60)
    recent = df[df['timestamp'] > one_min_ago]
    return min(len(recent) * 2, 10)

def is_locked_down():
    return os.path.exists(LOCKDOWN_FLAG)

def trigger_lockdown(): 
    with open(LOCKDOWN_FLAG, "w") as f: f.write("LOCKED")

def reset_lockdown():
    if os.path.exists(LOCKDOWN_FLAG): os.remove(LOCKDOWN_FLAG)

def generate_pdf_report(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, "CASB Security Audit Report", ln=True, align='C')
    pdf.set_font("helvetica", size=10)
    pdf.ln(10)
    for _, row in df.iterrows():
        pdf.cell(0, 10, f"{row['timestamp']} | {row['reason']} | {row['file']}", ln=True)
    
    # Convert bytearray to bytes to satisfy Streamlit's validator
    return bytes(pdf.output())