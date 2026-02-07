import streamlit as st
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import os
import sys
import pandas as pd

# 1. FORCE PATH INJECTION 
# This ensures that Streamlit can find 'utils.py' in the same folder.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from utils import (
    load_logs, 
    get_risk_score, 
    is_locked_down, 
    reset_lockdown, 
    generate_pdf_report, 
    ensure_dirs, 
    CLOUD_DIR, 
    FEED_PATH
)

# --- APP CONFIGURATION ---
st.set_page_config(page_title="CASB Security Sentinel", layout="wide", page_icon="🛡️")

# Refresh the dashboard every 2 seconds to show live updates.
st_autorefresh(interval=2000, key="f5_refresh")

# Ensure all necessary directories exist on startup.
ensure_dirs()

# --- 2. LOCKDOWN OVERLAY ---
# If the risk score hits 10, the scanner triggers a lockdown flag.
if is_locked_down():
    st.error("# 🚨 CRITICAL SYSTEM LOCKDOWN")
    st.warning("Automated Data Leakage Prevention is active. The scanner has been paused.")
    if st.button("🔓 AUTHORIZED ADMIN RESET"):
        reset_lockdown()
        st.success("System reset. Restarting scanner...")
        st.rerun()
    st.stop()  # Stops the rest of the dashboard from rendering.

# --- 3. HEADER & RISK GAUGE ---
st.title("🛡️ CASB SOC Management Console")
df = load_logs()
risk = get_risk_score()

col_gauge, col_metrics = st.columns([2, 1])

with col_gauge:
    # Gauge color shifts from green to red based on risk intensity.
    gauge_color = "red" if risk >= 8 else "orange" if risk >= 5 else "green"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        title={'text': f"Risk Level: {gauge_color.upper()}"},
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'color': gauge_color},
            'steps': [
                {'range': [0, 5], 'color': "lightgray"},
                {'range': [5, 8], 'color': "gray"}
            ]
        }
    ))
    fig.update_layout(height=350, margin=dict(t=50, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col_metrics:
    st.write("### Quick Stats")
    st.metric("Total Incidents Detected", len(df))
    st.metric("Files Currently Quarantined", len(df))
    
    # --- PDF EXPORT BUTTON ---
    # The bytes(pdf.output()) in utils.py fixes the 'bytearray' error.
    if not df.empty:
        try:
            pdf_bytes = generate_pdf_report(df)
            st.download_button(
                label="📥 Export Security Audit (PDF)",
                data=pdf_bytes,
                file_name=f"casb_audit_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"PDF Tool Error: {e}")

# --- 4. DATA TABLES & LIVE FEED ---
st.divider()
col_audit, col_feed = st.columns([2, 1])

with col_audit:
    st.subheader("📋 Incident Audit Trail")
    if df.empty:
        st.info("No threats detected yet. The system is clean.")
    else:
        # Show newest incidents at the top.
        st.dataframe(
            df.sort_values(by="timestamp", ascending=False), 
            use_container_width=True,
            hide_index=True
        )

with col_feed:
    st.subheader("📡 Live Threat Feed")
    with st.container(height=350, border=True):
        if os.path.exists(FEED_PATH):
            with open(FEED_PATH, "r") as f:
                # Reverse lines to show the latest activity first.
                lines = f.readlines()[::-1]
                for line in lines:
                    st.caption(line.strip())
        else:
            st.write("Waiting for scanner events...")

# --- 5. SIDEBAR SIMULATION TOOLS ---
st.sidebar.header("Simulation Control")
st.sidebar.info("Use these tools to test the CASB logic.")

if st.sidebar.button("🚀 Inject SSN Leak"):
    # Creates a file that the scanner will catch and quarantine.
    ts = pd.Timestamp.now().strftime('%H%M%S')
    test_file_path = os.path.join(CLOUD_DIR, f"threat_sim_{ts}.txt")
    
    with open(test_file_path, "w") as f:
        f.write("OFFICER NOTE: Found sensitive data. SSN: 000-00-0000")
    
    st.sidebar.success(f"Injected: threat_sim_{ts}.txt")

if st.sidebar.button("💳 Inject Credit Card Leak"):
    ts = pd.Timestamp.now().strftime('%H%M%S')
    test_file_path = os.path.join(CLOUD_DIR, f"cc_leak_{ts}.txt")
    
    with open(test_file_path, "w") as f:
        f.write("Transaction Record: User card 4111-1111-1111-1111")
    
    st.sidebar.success(f"Injected: cc_leak_{ts}.txt")

st.sidebar.divider()
st.sidebar.caption("CASB Project v1.0 - SOC Simulation")