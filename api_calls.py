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
    asd = len(serialnumbers)
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
            "desolvingSerialNumber": 2,     # 0 = Product structure is NOT resolved
                                            # 1 = Product structure is resolved UPWARD/DOWNWARD
                                            # 2 = Product structure is resolved DOWNWARD only
            "desolvingLevel": 0,            # 0 = Data of all work steps
                                            # 1 = Data of the work steps with station
                                            # 2 = Data of the work steps with the station and orientation
            "bookingResultKeys": ["BOOK_DATE", "STATION_DESC", "BOOK_STATE"]
        }

        response = requests.post(f"{SERVER_URL}/trGetSerialNumberHistoryData", json=payload)

        # 🔹 Handle the response
        if response.status_code == 200:
            results[serial] = response.json()
            # print("Serial Number History Data:", results[serial])
        else:
            results[serial] = f"Error {response.status_code}: {response.text}"
            print(f"Error: {response.status_code}, {response.text}")
        print(serial, ": Done!",asd, "serial numbers left!")
        asd = asd - 1

    return results

def lockObjects(session, station, serialnumbers):
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
            "unlockInformation": "Reason for unblocking",
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
