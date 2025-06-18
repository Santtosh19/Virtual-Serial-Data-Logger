# === Section 1: Import the necessary toolkits ===
import serial  # This is the library for serial port communication
import time    # This library lets us pause the program
import random  # This library helps us generate random numbers to make our data realistic

# === Section 2: Configuration ===
# Here we define our settings. It's good practice to keep them at the top.
SERIAL_PORT = 'COM5'    # This is the port our "device" will send data TO.
BAUD_RATE = 9600        # The speed of communication. Must match the listener later.

# === Section 3: The Main Program ===
print("--- Device Emulator Started ---")
print(f"Attempting to connect to serial port {SERIAL_PORT}...")

# This is a robust way to open the serial port.
# The 'try...except' block catches errors, and the 'finally' block ensures we close the port.
try:
    # This line opens the connection to our virtual phone jack 'COM5'
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
    print(f"Successfully connected to {SERIAL_PORT}. Sending data...")

        # === FORCED FAILURE TEST SEQUENCE ===
    print("\n--- RUNNING FORCED FAILURE SEQUENCE ---")

    # Helper function to make sending easier
    def send_data(temp, voltage, status):
        data_string = f"T:{temp:.2f},V:{voltage:.2f},S:{status}\n"
        ser.write(data_string.encode('utf-8'))
        print(f"Sent: {data_string.strip()}")
        time.sleep(1)

    # 1. Normal data
    send_data(50.0, 5.0, "NORMAL")
    send_data(52.0, 5.1, "NORMAL")

    # 2. Force a CRITICAL temperature breach
    print(">>> Forcing a Temperature Anomaly...")
    send_data(95.5, 5.0, "FORCED_TEMP_HIGH") 

    # 3. Force a CRITICAL voltage spike
    print(">>> Forcing a Voltage Anomaly...")
    send_data(60.0, 6.1, "FORCED_VOLTAGE_SPIKE")

    # 4. Force a RATE OF CHANGE anomaly (sudden drop)
    print(">>> Forcing a Rate of Change Anomaly...")
    send_data(25.0, 5.0, "FORCED_ROC_DROP") # 95.5 -> 25.0 is a huge drop!

    # 5. Force a HEARTBEAT LOSS anomaly
    print(">>> Forcing a Heartbeat Loss Anomaly...")
    time.sleep(5) # Just wait for 5 seconds
    send_data(55.0, 5.0, "RECONNECTED")

    print("\n--- FORCED FAILURE SEQUENCE COMPLETE ---")

    # while True: ... the rest of your old code ...

    # # This 'while True' loop will run forever, just like a real device.
    # while True:
    #     # --- This section simulates different device states ---
    #     # We'll generate a random number to decide which state to be in.
    #     choice = random.random() # Generates a number between 0.0 and 1.0

    #     if choice < 0.90: # 90% chance of being in NORMAL state
    #         temp = random.uniform(40.0, 55.0)  # Temperature in a normal range
    #         voltage = random.uniform(4.9, 5.1) # Voltage is stable
    #         status_code = "NORMAL"
    #         sleep_time = 1 # Send data every 1 second

    #     elif choice < 0.97: # 7% chance of being in a WARNING state
    #         temp = random.uniform(75.0, 85.0) # Temperature is getting hot!
    #         voltage = random.uniform(4.8, 5.2)
    #         status_code = "WARNING_TEMP_HIGH"
    #         sleep_time = 1

    #     elif choice < 0.99: # 2% chance of being in a CRITICAL state
    #         temp = random.uniform(50.0, 60.0)
    #         voltage = random.uniform(5.8, 6.2) # Voltage is dangerously high!
    #         status_code = "CRITICAL_VOLTAGE_SPIKE"
    #         sleep_time = 1

    #     else: # 1% chance of an "offline" or "heartbeat loss" failure
    #         print("[SIMULATING DEVICE OFFLINE... NO DATA FOR 5 SECONDS]")
    #         time.sleep(5)
    #         continue # Skip the rest of this loop and start a new one

    #     # Format our data into a single string. f-strings are great for this.
    #     # The '\n' at the end is a "newline" character. It's like pressing Enter.
    #     data_string = f"T:{temp:.2f},V:{voltage:.2f},S:{status_code}\n"

    #     # Send the data!
    #     # Computers send bytes, not letters, so we must .encode() our string into bytes.
    #     ser.write(data_string.encode('utf-8'))

    #     # Print to our own console so we can see what's being sent.
    #     print(f"Sent: {data_string.strip()}") # .strip() removes the newline for cleaner printing

    #     # Wait for a moment before sending the next piece of data.
    #     time.sleep(sleep_time)

# This 'except' block will run if the 'try' block fails (e.g., COM5 is busy).
except Exception as e:
    print(f"\n[ERROR] Could not open port '{SERIAL_PORT}'. Is it created and not in use by another program?")
    print(e)
except KeyboardInterrupt:
    # This allows us to stop the script cleanly by pressing Ctrl+C.
    print("\n--- Device Emulator Stopped by User ---")
finally:
    # This 'finally' block runs no matter what, even if there was an error.
    # It's crucial for making sure we always "hang up the phone" properly.
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"Serial port {SERIAL_PORT} closed.")