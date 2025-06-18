# High-Fidelity Reliability Monitoring Pipeline for Serial Data

## 🌟 Project Overview

This project is an advanced, end-to-end simulation of a production monitoring system for critical hardware. It is engineered from the ground up to demonstrate and explore core principles of **Site Reliability Engineering (SRE)** and **Systems Engineering**.

The pipeline encompasses the entire data lifecycle:
1.  **Data Generation:** A dynamic Python script emulates a hardware device, broadcasting a continuous stream of sensor data (temperature, voltage, status) over a virtual serial port. The emulator is designed to produce a realistic mix of `NORMAL`, `WARNING`, `CRITICAL`, and `OFFLINE` operational states.
2.  **Data Ingestion & Processing:** A robust, fault-tolerant logging service listens in real-time. It maintains an immutable raw audit log for data integrity while simultaneously parsing, validating, and structuring the data into a clean, analytics-ready format.
3.  **Anomaly Detection:** A sophisticated detection engine analyzes the structured data to identify a wide range of failure modes. This goes beyond simple checks to include predictive and availability-focused analysis.
4.  **Actionable Alerting:** The system culminates in the generation of a structured `JSON` report, detailing every detected anomaly. This machine-readable format is designed for integration with automated incident management and response systems.

---

## 🚀 Core Features & Demonstrated Skills

This project was built to showcase a deep understanding of the following professional concepts:

*   **Failure Mode Emulation:** The device emulator (`emulator.py`) doesn't just produce random numbers; it actively simulates a variety of real-world failure scenarios, proving the monitoring system's effectiveness.
*   **Data Integrity & Auditing:** The logging service (`logger_service.py`) separates raw, immutable logs (`raw.log`) from processed data. This is a critical practice for post-incident forensics and allows for data replay if the parsing logic is ever updated.
*   **Fault-Tolerant Design:** The ingestion pipeline is built with robust error handling (`try...except` blocks) to ensure that corrupted or malformed data packets do not crash the service. The system logs the error and continues, demonstrating resilience.
*   **Predictive Anomaly Detection:** The detector identifies not just static threshold breaches, but also **rate-of-change anomalies**. This represents a shift from reactive to proactive monitoring, allowing for intervention *before* a critical failure occurs.
    *   **Example:** A temperature reading that is still within "safe" limits but is rising at an alarming rate will be flagged as a `WARNING`.
*   **Availability Monitoring:** The system implements **heartbeat detection** to monitor the data source's availability. A loss of signal is treated as a critical incident, reflecting a focus on uptime as a primary metric.
*   **Structured, Actionable Alerting:** The final output is a `JSON` report (`anomaly_report.json`), not just a simple text log. This demonstrates an understanding of how monitoring systems integrate into a larger, automated **DevOps toolchain** (e.g., PagerDuty, Jira, Grafana).

---

## 🏗️ System Architecture & Data Flow

The project operates as a linear pipeline, where data is progressively refined and analyzed at each stage.
+------------------+ (Multi-state data stream) +-------------------+
| Python Device | ----------------------------------------->| Virtual Port 1 |
| Emulator Script | "T:85.5,V:5.0,S:WARNING_TEMP..." | (COM5) |
| (emulator.py) | +-------------------+
+------------------+ ^
|
VIRTUAL "CABLE"
(Created by Eltima VSPD
or com0com)
|
v
+-----------------------------+ (Listens in real-time, +-------------------+
| Real-time Logger & | validates, & parses) | Virtual Port 2 |
| Parser Service (Python) | <---------------------------------+ (COM6) |
| (logger_service.py) | +-------------------+
+-----------------------------+
| |
| (Immutable Audit Trail) | (Analytics-Ready Data)
v v
+------------+ +-------------------------+ +----------------------+
| Raw Log | | Structured Metrics File | | Parser Error Log |
| (raw.log) | | (structured_metrics.csv)| | (parser_errors.log) |
+------------+ +-------------------------+ +----------------------+
^
|
| (Analyzes entire dataset for trends and events)
|
+---------------------------------+
| Python Reliability |
| Anomaly Detection Engine |
| (detector.py) |
+---------------------------------+
|
| (Generates a machine-readable incident report)
v
+-----------------------------+
| JSON Anomaly Report |
| (anomaly_report.json) |
+-----------------------------+
---
## 📈 Example Results & Anomaly Detection in Action

After running the system with a "forced failure" sequence, the detection engine produces the following detailed `anomaly_report.json`:

```json
[
    {
        "timestamp": "2023-10-27T14:30:15.123456",
        "type": "THRESHOLD_BREACH_TEMP",
        "severity": "CRITICAL",
        "description": "Temperature 95.50°C exceeded threshold of 80.0°C."
    },
    {
        "timestamp": "2023-10-27T14:30:16.123456",
        "type": "THRESHOLD_BREACH_VOLTAGE",
        "severity": "CRITICAL",
        "description": "Voltage 6.10V was outside the normal range of 4.5V-5.5V."
    },
    {
        "timestamp": "2023-10-27T14:30:17.123456",
        "type": "RAPID_CHANGE_TEMP",
        "severity": "WARNING",
        "description": "Temperature changed by -70.50°C, exceeding the rate-of-change threshold of 15.0°C."
    },
    {
        "timestamp": "2023-10-27T14:30:22.123456",
        "type": "HEARTBEAT_LOSS",
        "severity": "CRITICAL",
        "description": "No data received for 5.0 seconds. Device may be offline."
    }
]

# 🛠️ Technical Deep Dive & Setup

This project is built with Python 3 and runs locally on a Windows machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Git**
- **Virtual Serial Port Tool**: A tool is required to create the virtual communication bridge.

  - **Recommended**: [Virtual Serial Port Driver by Eltima](https://www.eltima.com/products/vspdxp/) (The free version allows for one pair, which is sufficient for this project).
  - **Alternative**: [com0com](https://sourceforge.net/projects/com0com/) (A powerful open-source tool, but may require enabling "Test Mode" on modern versions of Windows due to driver signing policies).

## Local Setup & Execution

### 1. Configure Virtual Ports

Using your chosen tool, create a virtual serial port pair: `COM5 <-> COM6`. Ensure the ports are active and visible in Windows Device Manager.

### 2. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/YourUsername/Your-Repo-Name.git
cd Your-Repo-Name


3. Set Up Virtual Environment
It is critical to use a virtual environment to manage dependencies and avoid conflicts.

# Create the virtual environment folder named 'venv'
python -m venv venv

# Activate the environment
.\venv\Scripts\activate

4. Install Dependencies
Install all required packages from the requirements.txt file:

pip install -r requirements.txt

Running the Full Pipeline
You will need at least two terminals, both with the virtual environment (venv) activated.

1. Terminal 1: Start the Device Emulator
This script will start broadcasting data immediately: python emulator.py

2. Terminal 2: Start the Logging Service
This service will listen for the data, create the log files, and process data as it arrives: python logger_service.py

3. Terminal 3 (or reuse one): Run the Analysis
Execute the detection engine on the collected data: python detector.py

This final step reads structured_metrics.csv and generates anomaly_report.json if anomalies are found.

4. Let the System Run
Allow the scripts to run for 60-120 seconds to accumulate a meaningful dataset. Observe the real-time output in both terminals.

5. Stop the Services
Press Ctrl+C in both terminals to stop the scripts gracefully.

🔮 Future Improvements & Potential Extensions
This project provides a solid foundation that could be extended in many professional directions:

Database Integration: Replace the CSV file storage with a time-series database like InfluxDB or Prometheus for more efficient querying and data retention.

Real-time Dashboarding: Use a tool like Grafana to connect to the database and build live dashboards that visualize the temperature, voltage, and display alerts as they happen.

Alerting Integration: Write a small script that "watches" for changes to anomaly_report.json and makes a real API call to a service like Twilio (for SMS alerts) or the PagerDuty API.

Configuration Management: Move all thresholds and settings (COM ports, file names, etc.) out of the Python scripts and into a separate config.ini or config.yaml file, making the system easier to configure without changing the code.
