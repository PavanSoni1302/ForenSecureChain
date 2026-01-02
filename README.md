# ForenSecureChain: AI-Driven Fileless Malware & Memory Forensics Platform
**Status:** 🚧 Phase 1 Complete (Infrastructure & Log Pipeline)

## 📌 Project Overview
ForenSecureChain is a cybersecurity research project designed to detect **Fileless Malware** using Artificial Intelligence and secure the evidence using **Blockchain Technology**.

This repository hosts the configuration, simulation scripts, and analysis engines for the platform.

## 🏗️ Architecture Setup (Current Progress)
I have designed and deployed a custom **Cyber Range** to simulate and analyze attacks.

### 1. Lab Infrastructure (Virtual Environment)
* **Hypervisor:** VirtualBox
* **Network:** Isolated Host-Only Network (10.0.2.x range) for safe malware execution.

### 2. The Machines
| Role | OS | IP Address | Function |
| :--- | :--- | :--- | :--- |
| **Attacker** | Kali Linux | *Dynamic* | Penetration testing & payload delivery |
| **Victim** | Windows 10 | 10.0.2.6 | The target machine running Sysmon & Winlogbeat |
| **Server** | Ubuntu Server | 10.0.2.5 | Hosts the ELK Stack (Elasticsearch & Kibana) |
| **Backup** | Windows 11 | *Planned* | Secondary target |

### 3. Telemetry & Monitoring
* **Sysmon:** Installed on the Victim machine to capture deep-level system logs (Process creation, Network connections).
* **Winlogbeat:** Configured to ship logs in real-time to the Ubuntu Server.
* **ELK Stack:** Elasticsearch and Kibana configured for log indexing and visualization.

## ⚔️ Simulation & Testing
* **Current Test:** `certutil` LOLBin (Living off the Land) download attack.
* **Status:** Log pipeline successfully verified. `certutil` commands are being captured and indexed.

## 🚀 Next Steps
* [ ] Generate dataset using varied fileless attacks (PowerShell, WMI).
* [ ] Build Python parser to extract features from Elasticsearch.
* [ ] Develop AI Model (Scikit-Learn) for anomaly detection.
* [ ] Implement Blockchain hashing for log integrity.