import requests
import json
from config import SERVER_URL


def functions():
    response = requests.get(SERVER_URL)

    if response.status_code == 200:
        functions_list = response.json()
        print(functions_list)
    else:
        print(f"Error: {response.status_code}")


def login(username, password):
    login_data = {
        "sessionValidationStruct": {
            "stationNumber": "",
            "stationPassword": "",
            "user": username,
            "password": password,
            "client": "01",
            "registrationType": "U",  # U = User login, S = Station login
            "systemIdentifier": "http://ves1-itacv2-02.vnet.valeo.com:8080"
        }
    }

    # Send the request
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{SERVER_URL}/regLogin", data=json.dumps(login_data), headers=headers)

    # Handle response
    if response.status_code == 200:
        session_info = response.json()
        session_context = session_info.get("result", {}).get("sessionContext", {})
        session_id = session_context.get("sessionId")
        person_id = session_context.get("persId")
        locale = session_context.get("locale")
        print(f"Login successful! Session ID: {session_id}")

        return [session_id, person_id, locale]

    else:
        print(f"Login failed: {response.status_code}, {response.text}")


def logout(session):
    logout_data = {
        "sessionContext":{
            "sessionId": session[0],
            "persId": session[1],
            "locale": session[2]
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{SERVER_URL}/regLogout", data=json.dumps(logout_data), headers=headers)

    if response.status_code == 200:
        logout_info = response.json().get("result", {}).get("return_value", {})
        print("Logged out!", logout_info)
    else:
        print(f"Error: {response.status_code}, {response.text}")


def trGetSerialNumberHistoryData(session, station, serialnumbers):
    results = {}
    counter = len(serialnumbers)
    for serial in serialnumbers:
        payload = {
            "sessionContext": {
                "sessionId": session[0],
                "persId": session[1],
                "locale": session[2]
            },
            "stationNumber": station,
            "serialNumber": serial,
            "serialNumberPos": "",
            "processLayer": 2,
            "desolvingSerialNumber": 2,
            "desolvingLevel": 0,
            "bookingResultKeys": ["STATION_NUMBER", "BOOK_DATE", "STATION_DESC", "BOOK_STATE", "SEQUENCE_NUMBER"]
        }

        response = requests.post(f"{SERVER_URL}/trGetSerialNumberHistoryData", json=payload)

        if response.status_code == 200:
            results[serial] = response.json()
        else:
            results[serial] = f"Error {response.status_code}: {response.text}"
            print(f"Error: {response.status_code}, {response.text}")
        print(serial, ": Done!",counter, "serial numbers left!")
        counter = counter - 1

    return results


def lockObjects(session, station, serialnumbers):
    results = {}
    counter = len(serialnumbers)

    for serial in serialnumbers:
        payload = {
            "sessionContext": {
                "sessionId": session[0],
                "persId": session[1],
                "locale": session[2]
            },
            "stationNumber": station,
            "objectType": 0,
            "lockGroupName": "Pressure 2X fail",
            "lockInformation": "Rewelding",
            "lockDate": -1,
            "lockDependencies": 0,
            "objectUploadKeys": ["ERROR_CODE","SERIAL_NUMBER"],
            "objectUploadValues": [0, serial]
        }

        response = requests.post(f"{SERVER_URL}/lockObjects", json=payload)

        if response.status_code == 200:
            results[serial] = response.json()
        else:
            results[serial] = f"Error: {response.status_code}: {response.text}"

        print(serial, ": Done!", counter, "serial numbers left!")
        counter = counter - 1

    return results


def lockUnlockObjects(session, station, serialnumbers):
    results = {}

    for serial in serialnumbers:
        payload = {
            "sessionContext": {
                "sessionId": session[0],
                "persId": session[1],
                "locale": session[2]
            },
            "stationNumber": station,
            "objectType": 0,
            "lockGroupName": -1,
            "unlockInformation": "Reason for unlocking",
            "unlockCompleteGroup": 0,
            "unlockDate": -1,
            "lockDependencies": 0,
            "objectUploadKeys": ["ERROR_CODE","SERIAL_NUMBER"],
            "objectUploadValues": [0, serial]
        }

        response = requests.post(f"{SERVER_URL}/lockUnlockObjects", json=payload)

        if response.status_code == 200:
            results[serial] = response.json()
        else:
            results[serial] = f"Error: {response.status_code}: {response.text}"

    return results


def lockGetLockedObjects(session, station, serialnumbers):
    results = {}

    for serial in serialnumbers:
        payload = {
            "sessionContext": {
                "sessionId": session[0],
                "persId": session[1],
                "locale": session[2]
            },
            "stationNumber": station,
            "objectType": 0,
            "lockGroupName": "Test",
            "lockInformation": "Reason for blocking",
            "lockDate": -1,
            "lockDependencies": 0,
            "objectUploadKeys": ["ERROR_CODE","SERIAL_NUMBER"],
            "objectUploadValues": [0, serial]
        }

        response = requests.post(f"{SERVER_URL}/lockObjects", json=payload)

        if response.status_code == 200:
            results[serial] = response.json()
        else:
            results[serial] = f"Error: {response.status_code}: {response.text}"

    return results


def shipGetSerialNumberDataForShippingLot(session, station, lotnumbers):
    results = {}

    for lot in lotnumbers:
        payload = {
            "sessionContext": {
                "sessionId": session[0],
                "persId": session[1],
                "locale": session[2]
            },
            "stationNumber": station,
            "lotNumber": lot,
            "serialNumberResultKeys": ["SERIAL_NUMBER", "SHIPPING_DATE"]
        }

        response = requests.post(f"{SERVER_URL}/shipGetSerialNumberDataForShippingLot", json=payload)

        if response.status_code == 200:
            results[lot] = response.json()
        else:
            results[lot] = f"Error: {response.status_code}: {response.text}"

    return results


def trGetResultDataForSerialNumber(session, station, serialnumbers):
    results = {}
    counter = len(serialnumbers)
    for serial in serialnumbers:
        payload = {
            "sessionContext": {
                "sessionId": session[0],
                "persId": session[1],
                "locale": session[2]
            },
            "stationNumber": station,
            "serialNumber": serial,
            "serialNumberPos": -1,
            "processLayer": 2,
            "type": -1,
            "name": -1,
            "allProductEntries": 1,
            "onlyLastEntry": 1,                     # 0: mindegyik sequence;  1: utolsó sequence
            "resultDataKeys": ["DATE_CREATED", "MEASURE_NAME", "MEASURE_VALUE", "STATION_NUMBER"],
        }

        response = requests.post(f"{SERVER_URL}/trGetResultDataForSerialNumber", json=payload)

        # 🔹 Handle the response
        if response.status_code == 200:
            results[serial] = response.json()
            # print("Serial Number History Data:", results[serial])
        else:
            results[serial] = f"Error {response.status_code}: {response.text}"
            print(f"Error: {response.status_code}, {response.text}")

        counter = counter - 1
        print(serial, ": Done!", counter, "serial numbers left!")

    return results


def trGetMergeParts(session, station, serialnumbers):
    results = {}
    counter = len(serialnumbers)
    for serial in serialnumbers:
        payload = {
            "sessionContext": {
                "sessionId": session[0],
                "persId": session[1],
                "locale": session[2]
            },
            "stationNumber": station,
            "serialNumber": serial,
            "serialNumberPos": -1,
            "resolveDirection": 1,
            "resolveLevel": -1,
            "mergePartsResultKeys": ["SERIAL_NUMBER"]
        }

        response = requests.post(f"{SERVER_URL}/trGetMergeParts", json=payload)

        if response.status_code == 200:
            results[serial] = response.json()
        else:
            results[serial] = f"Error: {response.status_code}: {response.text}"

        print(serial, ": Done!", counter, "serial numbers left!")
        counter = counter - 1

    return results