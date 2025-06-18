# === Section 1: Import the necessary toolkits ===
import pandas as pd  # The powerful library for data analysis
from datetime import timedelta # Used for working with time differences
import json # For creating the JSON report file

# === Section 2: Configuration ===
CSV_FILE = 'structured_metrics.csv'
# --- Anomaly Detection thresholds ---
TEMP_THRESHOLD = 80.0  # Anything above this is a "critical" temperature
VOLTAGE_THRESHOLD_HIGH = 5.5
VOLTAGE_THRESHOLD_LOW = 4.5
TEMP_RATE_OF_CHANGE_THRESHOLD = 15.0 # A change of 15 degrees in one time step is a problem
HEARTBEAT_TIMEOUT_SECONDS = 4 # If we don't hear from the device for 4 seconds, it's an issue

# === Section 3: The Main Program ===
print("--- Anomaly Detection Engine Started ---")

try:
    # Use pandas to read our CSV into a 'DataFrame'.
    # A DataFrame is like a super-powered spreadsheet in memory.
    # We also tell it to understand that our 'timestamp' column contains dates and times.
    df = pd.read_csv(CSV_FILE, parse_dates=['timestamp'])

    # Make sure the data is sorted by time, just in case.
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    
    print(f"Successfully loaded {len(df)} records from '{CSV_FILE}'.")
    
    anomalies_found = [] # An empty list to store all the problems we find.

    # --- Detection Method 1: Simple Threshold Breaches ---
    # Find all rows where the temperature is above our threshold.
    temp_anomalies = df[df['temperature'] > TEMP_THRESHOLD]
    for index, row in temp_anomalies.iterrows():
        anomaly_details = {
            'timestamp': row['timestamp'],
            'type': 'THRESHOLD_BREACH_TEMP',
            'severity': 'CRITICAL',
            'description': f"Temperature {row['temperature']:.2f}°C exceeded threshold of {TEMP_THRESHOLD}°C."
        }
        anomalies_found.append(anomaly_details)
    
    # Do the same for voltage spikes.
    voltage_anomalies = df[(df['voltage'] > VOLTAGE_THRESHOLD_HIGH) | (df['voltage'] < VOLTAGE_THRESHOLD_LOW)]
    for index, row in voltage_anomalies.iterrows():
        anomaly_details = {
            'timestamp': row['timestamp'],
            'type': 'THRESHOLD_BREACH_VOLTAGE',
            'severity': 'CRITICAL',
            'description': f"Voltage {row['voltage']:.2f}V was outside the normal range."
        }
        anomalies_found.append(anomaly_details)

    # --- Detection Method 2: Rate-of-Change Anomalies ---
    # Calculate the difference in temperature between each row and the one before it.
    df['temp_change'] = df['temperature'].diff()
    
    # Find all rows where the change is greater than our threshold.
    roc_anomalies = df[df['temp_change'].abs() > TEMP_RATE_OF_CHANGE_THRESHOLD]
    for index, row in roc_anomalies.iterrows():
        anomaly_details = {
            'timestamp': row['timestamp'],
            'type': 'RAPID_CHANGE_TEMP',
            'severity': 'WARNING',
            'description': f"Temperature changed by {row['temp_change']:.2f}°C, exceeding the rate-of-change threshold."
        }
        anomalies_found.append(anomaly_details)

    # --- Detection Method 3: Heartbeat Loss Detection ---
    # Calculate the time difference between each row and the one before it.
    df['time_diff'] = df['timestamp'].diff()
    
    # Find all rows where the time gap is larger than our timeout.
    heartbeat_anomalies = df[df['time_diff'] > timedelta(seconds=HEARTBEAT_TIMEOUT_SECONDS)]
    for index, row in heartbeat_anomalies.iterrows():
        time_gap = row['time_diff'].total_seconds()
        anomaly_details = {
            'timestamp': row['timestamp'],
            'type': 'HEARTBEAT_LOSS',
            'severity': 'CRITICAL',
            'description': f"No data received for {time_gap:.1f} seconds. Device may be offline."
        }
        anomalies_found.append(anomaly_details)


    # === Section 4: Generate Reports ===
    print("\n--- ANOMALY REPORT (CONSOLE) ---")
    if anomalies_found:
        # Sort anomalies by time for a chronological report
        anomalies_found.sort(key=lambda x: x['timestamp'])
        
        # 1. Print the human-readable report to the console
        for anomaly in anomalies_found:
            # We need to convert the timestamp object to a string for printing
            ts_str = anomaly['timestamp'].isoformat()
            print(f"[{ts_str}]-[{anomaly['severity']}]-[{anomaly['type']}] : {anomaly['description']}")

        # 2. Create the machine-readable JSON report
        # We need to prepare the data for JSON, as it doesn't understand pandas timestamps directly.
        json_report_data = []
        for anomaly in anomalies_found:
            json_report_data.append({
                'timestamp': anomaly['timestamp'].isoformat(), # Convert timestamp to a standard string
                'type': anomaly['type'],
                'severity': anomaly['severity'],
                'description': anomaly['description']
            })

        # Write the data to a .json file
        try:
            with open('anomaly_report.json', 'w') as f:
                # json.dump writes the data.
                # 'indent=4' makes the file easy for humans to read ("pretty-printing").
                json.dump(json_report_data, f, indent=4)
            print("\n--- Successfully generated 'anomaly_report.json' ---")
        except Exception as e:
            print(f"\n[ERROR] Could not write JSON report: {e}")

    else:
        print("No anomalies detected. System is operating normally.")

except FileNotFoundError:
    print(f"[ERROR] Could not find the file '{CSV_FILE}'. Please run the logger_service.py first to generate data.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")