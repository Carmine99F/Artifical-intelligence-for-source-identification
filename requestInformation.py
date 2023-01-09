from textwrap import indent
import requests
import json
import config
import calcoloProbabilità as cp
"""_summary_
La funzione prende come parametro il nome di una centralina e restituisce un dizionario con le info relative 
alla direzione_vento,gas_resistance,intensita_vento,pm10,pm2_5
"""

def getInfo(nameCentralina,data1,data2):
    url="https://square.sensesquare.eu:5001/download"
    print("request")
    dati={
        "apikey":"WDBNX4IUF66C",
         "req_type":"daily",#daily,hourly
         "zoom":5,
        "start_hour":00,
         "end_hour":23,
         "format":"json",
         "fonti":"[ssq]",
         "req_centr":nameCentralina,
         "start_date":data1,
         "end_date":data2
    }
    response=requests.post(url,data=dati)
    if response.status_code==200:
         #print(response.text)
         if response.text != "":
             #arrayInfoCentraline=[]
            infoJson=json.loads(str(response.text))
            dataJson={}
            if "direzione_vento" in infoJson.keys():
                if float(infoJson["direzione_vento"])<=7:
                    dataJson["direzione_vento"]=float(infoJson["direzione_vento"])+8
                if float(infoJson["direzione_vento"])>=8:
                    dataJson["direzione_vento"]=float(infoJson["direzione_vento"])-8
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
            pg=cp.dailyPercentage('ITLOMBAS123456','ITLOMBAS234567', 'ITLOMBAS334567')
            dataJson["percentuale_giornaliera"]=pg
            return dataJson
    else:
        raise Exception("Request failed. Status code ",response.status_code)
        print("Request failed")
        return None
   

#getInfo("ITLOMBAS123456",config.data,config.data)