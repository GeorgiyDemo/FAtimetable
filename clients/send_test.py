import requests

r = requests.get("http://77.37.132.120:5554/SendSMS/user=&password=123456&phoneNumber=+79999645590&msg=KOT").text
print(r.text)