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
        "start_date":"2022-01-08",
        "end_date":"2022-01-08"
    }
    response=requests.post(url,data=dati)
    if response.text != "":
        arrayInfoCentraline=[]
        infoJson=json.loads(str(response.text))
        dataJson={}
        if "direzione_vento" in infoJson.keys():
            dataJson["direzione_vento"]=float(infoJson["direzione_vento"])
            dataJson["direzione_vento_gradi"]=float(infoJson["direzione_vento"])*22.5
        if "gas_resistance" in infoJson.keys():
            dataJson["gas_resistance"]=float(infoJson["gas_resistance"])
        if "intensita_vento" in infoJson.keys():
            dataJson["intensita_vento"]=float(infoJson["intensita_vento"])
        if "pm10" in infoJson.keys():
            dataJson["pm10"]=float(infoJson["pm10"])
        if "pm2_5" in infoJson.keys():
            dataJson["pm2_5"]=float(infoJson["pm2_5"])
        if "ID" in infoJson.keys():
            dataJson["id"]=infoJson["ID"]
        return dataJson
    else:
        print("Response vuota")
        return None

