import csv
import os
from datetime import datetime, timezone
import pytz

def convert_to_custom_format(timestamp_ms):
    timestamp_sec = int(timestamp_ms) / 1000
    cet = pytz.timezone("Europe/Budapest")

    dt_utc = datetime.fromtimestamp(timestamp_sec, tz=timezone.utc)  # Convert from timestamp to UTC
    dt_cet = dt_utc.astimezone(cet)  # Convert to CET/CEST

    return dt_cet.strftime("%Y-%m-%d %H:%M:%S")


def convert_to_iso(timestamp_ms):
    timestamp_sec = int(timestamp_ms) / 1000
    cet = pytz.timezone("Europe/Budapest")

    dt_utc = datetime.fromtimestamp(timestamp_sec, tz=timezone.utc)  # Convert from timestamp to UTC
    dt_cet = dt_utc.astimezone(cet)  # Convert to CET/CEST

    return dt_cet.isoformat()  # Returns ISO 8601 format in CET/CEST


def history_find_aac(data):
    os.makedirs("history", exist_ok=True)
    output_file = f"history/aac_history_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv"

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Serial Number", "AAC", "State", "Timestamp"])  # Header

        for serial, details in data.items():
            values = details["result"]["bookingResultValues"]
            for i in range(0, len(values), 3):  # Process every 3 elements
                timestamp_ms, station_name, state = values[i:i + 3]
                if station_name.startswith("AAC"):
                    formatted_time = convert_to_custom_format(timestamp_ms)
                    state = "Pass" if state == "0" else "Fail"  # Convert state

                    writer.writerow([serial, station_name, state, formatted_time])  # Save to CSV
                    print(f"{serial} - {station_name} - {state} - {formatted_time}")  # Print to console


def history(data):
    os.makedirs("history", exist_ok=True)
    output_file = f"history/particle_history_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv"

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Serial Number", "Station", "State", "Timestamp"])  # Header

        for serial, details in data.items():
            values = details["result"]["bookingResultValues"]
            for i in range(0, len(values), 3):  # Process every 3 elements
                timestamp_ms, station_name, state = values[i:i + 3]
                if station_name.startswith("PCB1 Particle test"):
                    formatted_time = convert_to_custom_format(timestamp_ms)
                    state = "Pass" if state == "0" else "Fail"  # Convert state

                    writer.writerow([serial, station_name, state, formatted_time])  # Save to CSV
                    print(f"{serial} - {station_name} - {state} - {formatted_time}")  # Print to console

