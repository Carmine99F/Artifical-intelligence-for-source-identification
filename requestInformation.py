from textwrap import indent
import requests
import json
"""_summary_
La funzione prende come parametro il nome di una centralina e restituisce un dizionario con le info relative 
alla direzione_vento,gas_resistance,intensita_vento,pm10,pm2_5
"""
def getInfo(nameCentralina):
    url="https://square.sensesquare.eu:5001/download"
    dati={
        "apikey":"4BSFRYMNPZ0J",
        "req_type":"daily",#daily,hourly
        "zoom":5,
        "start_hour":00,
        "end_hour":23,
        "format":"json",
        "fonti":"ssq",
        "req_centr":nameCentralina,
        "start_date":"2022-03-29",
        "end_date":"2022-03-29"
    }
    response=requests.post(url,data=dati)
    if response.text != "":
        arrayInfoCentraline=[]
        infoJson=json.loads(str(response.text))
        dataJson={
                "direzione_vento":float(infoJson["direzione_vento"]),
                "gas_resistance":float(infoJson["gas_resistance"]),
                "intensita_vento":float(infoJson["intensita_vento"]),
                "pm10":float(infoJson["pm10"]),
                "pm2_5":float(infoJson["pm2_5"])
        }
        return dataJson
    else:
        print("Response vuota")
        return None

