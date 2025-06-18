# === Section 1: Import the necessary toolkits ===
import serial
import csv
from datetime import datetime
import time

# === Section 2: Configuration ===
SERIAL_PORT = 'COM6'      # This is the port we will LISTEN on.
BAUD_RATE = 9600
RAW_LOG_FILE = 'raw.log'  # The file for the raw, untouched data
CSV_FILE = 'structured_metrics.csv' # The file for the clean, parsed data
ERROR_LOG_FILE = 'parser_errors.log' # A file for any lines we can't understand

# === Section 3: Prepare the CSV File ===
# This part runs once at the beginning to set up our CSV file with headers.
try:
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        # These are the column titles
        writer.writerow(['timestamp', 'temperature', 'voltage', 'status_code'])
    print(f"'{CSV_FILE}' created with headers.")
except Exception as e:
    print(f"Error setting up CSV file: {e}")

# === Section 4: The Main Service Loop ===
print("--- Logger Service Started ---")
print(f"Listening on port {SERIAL_PORT}...")

try:
    # Open the port we are listening on
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

    while True:
        # Read one line of data from the serial port.
        # This will wait until it sees a newline character ('\n')
        line = ser.readline().decode('utf-8').strip()

        # Check if the line is not empty
        if line:
            # Get the current time with high precision
            timestamp = datetime.now().isoformat()
            
            # --- Task 1: Log the raw, untouched data for auditing ---
            try:
                with open(RAW_LOG_FILE, 'a') as raw_file:
                    raw_file.write(f"{timestamp} | {line}\n")
            except Exception as e:
                print(f"Error writing to raw log: {e}")


            # --- Task 2: Try to parse the data and log it to CSV ---
            # We put this in a 'try...except' block to be fault tolerant
            try:
                # Example line: "T:48.13,V:5.04,S:NORMAL"
                parts = line.split(',')
                # Check for correct format before trying to access indexes
                if len(parts) == 3 and parts[0].startswith('T:') and parts[1].startswith('V:') and parts[2].startswith('S:'):
                    temp_str = parts[0].split(':')[1]
                    volt_str = parts[1].split(':')[1]
                    status = parts[2].split(':')[1]

                    # Convert the string numbers into actual numbers (floats)
                    temp_float = float(temp_str)
                    volt_float = float(volt_str)
                    
                    # Write the clean data to our structured CSV file
                    with open(CSV_FILE, 'a', newline='') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow([timestamp, temp_float, volt_float, status])
                    
                    print(f"Logged: {timestamp}, {temp_float}, {volt_float}, {status}")

                else:
                    # If the line isn't in the format we expect, raise an error to be caught below
                    raise ValueError(f"Malformed data structure: {line}")

            except (ValueError, IndexError) as e:
                # If anything goes wrong in the 'try' block above, this code runs.
                error_message = f"{timestamp} | PARSE_ERROR | {e}\n"
                print(f"  [!] FAILED TO PARSE: {line}")
                
                # Log the specific error to our error log file.
                try:
                    with open(ERROR_LOG_FILE, 'a') as error_file:
                        error_file.write(error_message)
                except Exception as e:
                    print(f"Error writing to error log: {e}")
        
        # A small sleep to prevent the loop from running too fast if no data is coming in
        time.sleep(0.01)

except serial.SerialException as e:
    print(f"\n[ERROR] Could not open port '{SERIAL_PORT}'. Is the virtual port pair active?")
    print(e)
except KeyboardInterrupt:
    print("\n--- Logger Service Stopped by User ---")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"Serial port {SERIAL_PORT} closed.")