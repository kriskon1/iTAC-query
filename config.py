USERNAME = "..."
PASSWORD = "..."
SERVER_URL = "...../imsapi/rest/actions"

stationnumber = "xx-yy-zz"
serialnumbers = None

with open("serial.txt", mode="r") as file:
   serialnumbers = [line.strip() for line in file]
   print(f"Serial number reading done, total serial numbers: {len(serialnumbers)}")
