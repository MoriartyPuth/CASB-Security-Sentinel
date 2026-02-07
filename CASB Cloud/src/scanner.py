import os, re, shutil, time, sys

# Inject path so it can find utils.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import save_log_entry, get_risk_score, is_locked_down, trigger_lockdown, ensure_dirs, CLOUD_DIR, QUARANTINE_DIR

DLP_RULES = {
    "SSN_DETECTED": r"\b\d{3}-\d{2}-\d{4}\b",
    "CREDIT_CARD": r"\b(?:\d{4}[ -]?){3}\d{4}\b"
}

def start_engine():
    ensure_dirs()
    print(f"🛡️ Scanner Active. Monitoring: {CLOUD_DIR}")

    while True:
        if is_locked_down():
            time.sleep(2)
            continue

        if os.path.isdir(CLOUD_DIR):
            for filename in os.listdir(CLOUD_DIR):
                file_path = os.path.join(CLOUD_DIR, filename)
                if os.path.isdir(file_path): continue
                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        content = f.read()
                    for label, pattern in DLP_RULES.items():
                        if re.search(pattern, content):
                            save_log_entry(filename, label)
                            shutil.move(file_path, os.path.join(QUARANTINE_DIR, filename))
                            print(f" quarantined: {filename}")
                            break
                except Exception: pass

        if get_risk_score() >= 10:
            trigger_lockdown()
        time.sleep(1)

if __name__ == "__main__":
    start_engine()