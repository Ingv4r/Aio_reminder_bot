from datetime import datetime
date_string = "10.20"
try:
    datetime.strptime(date_string, f"%m.%d")
    print("Дата корректна")
    print(datetime.now())
except ValueError:
    print("Дата некорректна", datetime.now().year)