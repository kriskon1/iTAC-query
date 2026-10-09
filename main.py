import api_calls as ac
import filter
from config import USERNAME, PASSWORD, stationnumber, serialnumbers ##,lotnumbers


def main():
    # ac.functions()
    session = ac.login(USERNAME, PASSWORD)
    if session:
        # history = ac.trGetSerialNumberHistoryData(session, stationnumber, serialnumbers)
        # print(history)

        # lotinfo = ac.shipGetSerialNumberDataForShippingLot(session, stationnumber, lotnumbers)
        # filt = filter.serialnumbersinlot(lotinfo)
        # print(filt)

        # filter.history(history)
        # filter.history_2(history)
        # filter.history_find_aac(history)
        # filter.lotnumber(history)

        # lock = ac.lockObjects(session, stationnumber, serialnumbers)
        # print(filtered)
        # print(lock)

        merged = ac.trGetMergeParts(session, stationnumber, serialnumbers)
        filter.mergedfronthouse(merged)
        # print(merged)

        # measurement_data = ac.trGetResultDataForSerialNumber(session, "VES1-GEN603-130-01", serialnumbers)
        # print(measurement_data)
        # filter.measurement_results(measurement_data)

    else:
        print("Login failed. No session received.")
    ac.logout(session)

if __name__ == "__main__":
    main()
