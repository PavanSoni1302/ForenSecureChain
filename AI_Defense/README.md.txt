# 🛡️ ForenSecureChain: AI-Driven Malware Defense

## 📌 Project Overview
ForenSecureChain is a next-generation cybersecurity platform that combines **Real-Time Log Analysis** with **Machine Learning** to detect attacks that traditional antiviruses miss (like "Living off the Land" binaries).

## 🚀 Key Features
* **Live Threat Detection:** Monitors Windows events in real-time.
* **AI/ML Engine:** Uses a Random Forest model trained to recognize malicious command-line patterns.
* **Sysmon Integration:** Deep visibility into process creation events (Event ID 1).
* **Elastic Stack:** Centralized log aggregation using Elasticsearch and Winlogbeat.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **ML Libraries:** Scikit-Learn, Pandas, Joblib
* **Infrastructure:** Windows 10 (Victim), Ubuntu Server (SIEM)
* **Data Pipeline:** Winlogbeat -> Elasticsearch -> Python Engine

## 📂 Project Structure
* `detection_engine.py`: The main script that runs 24/7 monitoring.
* `force_train.py`: The training module that teaches the AI new threats.
* `random_forest_model.pkl`: The saved "Brain" of the AI.
* `winlogbeat.yml`: Configuration for log shipping.

## ⚡ How to Run
1. Start the Elasticsearch service on Ubuntu.
2. Run `python detection_engine.py` on the monitoring station.
3. Execute attacks on the victim machine to trigger alerts.

---
*Developed by Pavan Soni*