USERNAME = "KRISKON"
PASSWORD = "PASSWORD"
# SERVER_URL = "http://ves1-itacv2-02.vnet.valeo.com:8080/mes/imsapi/rest/actions"
SERVER_URL = "http://10.207.63.180:8080/mes/imsapi/rest/actions"


stationnumber = "VES1-GEN602-130-01"
# serialnumbers = ["C0640124345D47E0"]
# serialnumbers = ["C0640123273C098A"]
# serialnumbers = ["C0C5012524701F35"]
# lotnumbers = ["PE163902-2201,192,515507219"]

with open("serial.txt", mode="r") as file:
  serialnumbers = [line.strip() for line in file]
  # serialnumbers = [line.strip() for _, line in zip(range(10), file)]
  print(f"Serial number reading done, total serial numbers: {len(serialnumbers)}")

# with open("serial.txt", mode="r") as file:
#    lotnumbers = [line.strip() for line in file]
#    print(f"Lot number reading done, total lot numbers: {len(lotnumbers)}")
