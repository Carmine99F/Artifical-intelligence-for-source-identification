import requests

url="https://square.sensesquare.eu:5001/download"
dati={
        "apikey":"4BSFRYMNPZ0J",
        "req_type":"daily",#daily,hourly
        "zoom":5,
        "start_hour":0,
        "end_hour":23,
        "format":"json",
        "fonti":"ssq",
        "req_centr":"ITCAMMON234567",
        "start_date":"2022-03-27",
        "end_date":"2022-03-27"
    }

response=requests.post(url=url,data=dati)
if response.text== "":
    print("Vuota")
else:
    print("Non vuota")
#print(response.text)
