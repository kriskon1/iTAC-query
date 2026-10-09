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
    # return dt_cet.isoformat()  # Returns ISO 8601 format in CET/CEST


def history_find_aac(data):
    os.makedirs("history", exist_ok=True)
    output_file = f"history/aac_history_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv"

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Serial Number", "AAC", "State", "Timestamp"])  # Header

        for serial, details in data.items():
            values = details["result"]["bookingResultValues"]
            for i in range(0, len(values), 4):  # Process every 3 elements
                station_id, timestamp_ms, station_name, state = values[i:i + 4]
                if station_name.startswith("AAC"):
                    formatted_time = convert_to_custom_format(timestamp_ms)
                    state = "Pass" if state == "0" else "Fail"  # Convert state

                    writer.writerow([serial, station_name, state, formatted_time])  # Save to CSV
                    print(f"{serial} - {station_name} - {state} - {formatted_time}")  # Print to console


def history(data):
    os.makedirs("history", exist_ok=True)
    output_file = f"history/eol_history_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Serial Number", "Station", "State", "Timestamp", "Sequence number"])

        for serial, details in data.items():
            values = details["result"]["bookingResultValues"]
            for i in range(0, len(values), 5):
                try:
                   station_id, timestamp_ms, station_name, state, seq = values[i:i + 5]


                   if "Blemish" in station_name:
                        formatted_time = convert_to_custom_format(timestamp_ms)
                        state_text = "Pass" if state == "0" else "Fail"

                        writer.writerow([serial, station_name, state_text, formatted_time, seq])
                        # print(f"{serial} - {station_name} - {state_text} - {formatted_time} - {seq}")
                        break


                except ValueError:
                    continue


def lotnumber(data):
    os.makedirs("history", exist_ok=True)
    output_file = f"history/lotnumber_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv"

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Serial Number", "lotNumber"])  # Header

        for serial, details in data.items():
            values = details["result"]["lotNumber"]
            writer.writerow([serial, values])  # Save to CSV
            print(f"{serial} - {values}")  # Print to console


def serialnumbersinlot(data):
    os.makedirs("history", exist_ok=True)
    output_file = f"history/lot_info_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv"

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Product number", "Quantity", "LOT", "Serial number", "Packaging date"])

        for lot, details in data.items():
            new_lot = lot[1:]
            values = details["result"]["serialNumberResultValues"]
            for i in range(0, len(values), 2):
                serial, timestamp_ms = values[i:i + 2]
                formatted_time = convert_to_custom_format(timestamp_ms)
                writer.writerow([new_lot, serial, formatted_time])
                print(f"{new_lot} - {serial} - {formatted_time}")


def measurement_results(data):
    os.makedirs("history", exist_ok=True)
    output_file = f"history/measurement_info_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Serial", "Station", "Fill", "Leak", "Date"])

        for serial, details in data.items():
            values = details["result"]["resultDataValues"]
            for i in range(0, len(values), 4):
                ts, label, value, stn = values[i:i+4]

                if label == "Pressure":
                    fill = value
                    timestamp = convert_to_custom_format(ts)
                    station = stn
                    # sequence = seq

                if label == "Leak":
                    leak = value

            writer.writerow([serial, station, fill, leak, timestamp])
            print(serial, station, fill, leak, timestamp)


def mergedfronthouse(data):
    os.makedirs("history", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"history/merge_info_{timestamp}.csv"

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Serial number", "Front housing"])

        for serial, details in data.items():
            values = details.get("result", {}).get("mergePartsResultValues", [])
            found_value = "No merged units"
            for val in values:
                if val.startswith("C0C"):
                    found_value = val
                    break  # Stop at the first find

            writer.writerow([serial, found_value])


def history_2(data):
    os.makedirs("history", exist_ok=True)
    output_file = f"history/particle_history_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Serial Number", "Station", "State", "Timestamp"])

        for serial, details in data.items():
            values = details["result"]["bookingResultValues"]

            ves1_failures = []
            last_timestamp = ""
            has_ves1_station = False

            for i in range(0, len(values), 4):
                try:
                    station_id, timestamp_ms, station_name, state = values[i:i + 4]

                    if station_id.startswith("VES1-GEN6"):
                        has_ves1_station = True
                        last_timestamp = timestamp_ms  # Eltesszük az utolsó időbélyeget a Pass sorhoz

                        if state != "0":
                            ves1_failures.append((station_name, timestamp_ms))

                except ValueError:
                    continue

            # Csak azokkal a panelekkel foglalkozunk, amik jártak VES1-GEN6 állomáson
            if has_ves1_station:
                if len(ves1_failures) > 0:
                    # Volt hiba -> Kilistázzuk a hibás állomásokat
                    for station_name, t_ms in ves1_failures:
                        formatted_time = convert_to_custom_format(t_ms)  # A saját formázód
                        writer.writerow([serial, station_name, "Fail", formatted_time])
                        print(f"{serial} - {station_name} - Fail - {formatted_time}")
                else:
                    # Egyáltalán nincs hiba -> Szériaszám + Pass
                    formatted_time = convert_to_custom_format(last_timestamp)
                    writer.writerow([serial, "All VES1-GEN6", "Pass", formatted_time])
                    print(f"{serial} - All VES1-GEN6 - Pass - {formatted_time}")
