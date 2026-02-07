# Topic: The development and simulation of a Cloud Access Security Broker (CASB) focused on Data Loss Prevention (DLP) and Security Operations Center (SOC) management.

A real-time Cloud Access Security Broker (CASB) simulation that monitors cloud storage for sensitive data leaks (DLP), automates threat response, and provides a Live Security Operations Center (SOC) dashboard.

## 🚀 Overview

This project simulates how a CASB sits between users and cloud service providers to enforce security policies. It monitors a "Cloud" directory, detects PII (Personally Identifiable Information) like SSNs and Credit Card numbers, and automatically quarantines threats.

## 🔍 Key Features

-  Real-time DLP Scanner: Scans files for patterns (Regex) and moves compromised data to a secure quarantine folder.
               
- Live SOC Dashboard: Built with Streamlit to visualize risk levels, audit trails, and live activity feeds.

- Automated Response: Automatically triggers a System Lockdown if the threat velocity (Risk Score) exceeds a safety threshold.

- Audit Reporting: Generates downloadable PDF reports of all security incidents using fpdf2.

## 🛠️ Tech Stack 

- Language: Python 3.11+

- UI/Dashboard: Streamlit

- Data Analysis: Pandas

- Visualization: Plotly

- PDF Generation: FPDF2

## 🧪 How to Test

- Manual Leak: Drop a text file into cloud_storage containing SSN: 000-00-0000.

- Dashboard Simulation: Use the "Trigger Data Leak" button in the dashboard sidebar to inject threats automatically.

- Observation: Watch the file disappear from the cloud folder, move to quarantine, and appear in the Audit Log with an increased Risk Score.

- Lockdown: Inject 5+ threats rapidly to witness the Emergency Lockdown state.

## 📜 Security Policies (DLP Rules)

The system is currently configured to detect:

- US Social Security Numbers: \b\d{3}-\d{2}-\d{4}\b

- Credit Card Numbers: \b(?:\d{4}[ -]?){3}\d{4}\b

## 🛠️ Advanced Installation

Clone the Repository: https://github.com/MoriartyPuth/CASB-Security-Sentinel

Install Dependencies: pip install streamlit pandas plotly fpdf2 streamlit-autorefresh

## 📊 Vizualization

<img width="1917" height="961" alt="image" src="https://github.com/user-attachments/assets/1890983b-41ba-4722-9321-f33e70469535" />
