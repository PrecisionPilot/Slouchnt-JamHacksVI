from asyncio import SendfileNotAvailableError
import yagmail

sender_email = "seanwaterloo2997@gmail.com"
sender_password = ""
with open("Assets/password.txt", "r") as f:
    sender_password = f.read()

yag = yagmail.SMTP(user=sender_email, password=sender_password)

def send_email(rec, subj, content):
    yag.send(to=rec, subject=subj, contents=content)