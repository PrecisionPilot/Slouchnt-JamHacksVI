import smtp
import datetime

date = str(datetime.datetime.now())
date = date[0:10]

print(date)



with open("data.dat", "a") as f:
    f.write(date + "\n\n")