from datetime import date, timedelta
import requests
import json
import config
import calcoloProbabilità as cp
import pyautogui 
import ExceptionCustm 

class NumberSensorsInsufficient(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) :
        message="Il numero di centraline attive per il giorno {} è minore di 3".format(config.data)
        pyautogui.alert(message,"Errore ")


"""
    Restituisce il valore massimo dell'intesnità del vento relativo agli ultimi 15 giorni
"""

def getIntensitaVento(nameCentralina,data1,data2):
    config.counter=config.counter+1
    #("request ",config.counter)
    toDay=date.today()
    oldDate=toDay-timedelta(15)
    url="https://square.sensesquare.eu:5001/download"
    #print("request")
    dati={
        "apikey":"WDBNX4IUF66C",
         "req_type":"daily",#daily,hourly
         "zoom":5,
        "start_hour":00,
         "end_hour":23,
         "format":"json",
         "fonti":"[ssq]",
         "req_centr":nameCentralina,
         "start_date":str(oldDate),
         "end_date":str(toDay)
    }
    maxIntensitaVento=0
    response=requests.post(url,data=dati)
    if response.status_code==200:
         if response.text != "":
            arrayResponse=response.text.split("\n")
            del arrayResponse[-1]
            for item in arrayResponse:
                diz=json.loads(str(item))
                if float(diz["intensita_vento"]) > maxIntensitaVento:
                    maxIntensitaVento=float(diz["intensita_vento"])
            return maxIntensitaVento
    else:
        raise Exception("Request failed. Status code ",response.status_code)
        print("Request failed")
        return None

#getIntensitaVento("ITLOMBAS123456",config.data,config.data)
#getInfo('ITLOMBAS123456','ITLOMBAS234567','ITLOMBAS334567',config.data,config.data)


"""_summary_
La funzione prende come parametro il nome di una centralina e restituisce un dizionario con le info relative 
alla direzione_vento,gas_resistance,intensita_vento,pm10,pm2_5
"""

def getInfo2(idCentaline: list):
    dizionarioMediaGiornaliera={
    }
    url="https://square.sensesquare.eu:5001/download"
    for name in idCentaline:
        #dizionarioMediaGiornaliera.update({str(name):{}})
        coordCentralina=requests.post("https://square.sensesquare.eu:5002/informazioni_centralina", 
                      data={"apikey": "WDBNX4IUF66C", "ID": name})
        #print("coord centralina ")
        #print(coordCentralina.json()["result"])
        lat=coordCentralina.json()["result"]["lat"]
        lon=coordCentralina.json()["result"]["lon"]
        dati={
            "apikey":"WDBNX4IUF66C",
            "req_type":"daily",#daily,hourly
            "zoom":5,
            "start_hour":00,
            "end_hour":23,
            "format":"json",
            "fonti":"[ssq]",
            "req_centr":name,
            "start_date":config.data,
            "end_date":config.data
        }
        response=requests.post(url,data=dati)
        if response.status_code==200:
            if response.text != "":
                #print(response.text)
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
                dataJson["intensita_vento 15 giorni"]=getIntensitaVento(name,config.data,config.data)
                #print("Per la centralina ",name, " intensita 15 gionri vale  ", getIntensitaVento(name,config.data,config.data))
                dataJson["lat"]=lat
                dataJson["lon"]=lon
                #pg=cp.dailyPercentage(idCentaline)
                #dataJson["percentuale_giornaliera"]=pg
                dizionarioMediaGiornaliera[name]=dataJson
               
    config.dizMediaGiornaliera=dizionarioMediaGiornaliera
    print("len ", len(config.dizMediaGiornaliera))
    if len(config.dizMediaGiornaliera) < 3:
        raise NumberSensorsInsufficient()
    #print(json.dumps(config.dizMediaGiornaliera,indent=3))
         

#getInfo2(config.arrayNomiCentraline)
