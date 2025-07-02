import api_calls as ac
import filter
from config import USERNAME, PASSWORD, stationnumber, serialnumbers


def main():
    # ac.functions()
    session = ac.login(USERNAME, PASSWORD)
    if session:
        history = ac.trGetSerialNumberHistoryData(session, stationnumber, serialnumbers)
        # print(history)
        filtered = filter.history(history)
        print(filtered)
    else:
        print("Login failed. No session received.")
    ac.logout(session)

if __name__ == "__main__":
    main()
