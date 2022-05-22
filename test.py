import smtp
import datetime

date = str(datetime.datetime.now())
date = date[0:10]

print(date)



with open("Assets/data.dat", "a") as f:
    f.write(date + "\n\n")