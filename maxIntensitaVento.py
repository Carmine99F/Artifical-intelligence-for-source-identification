from datetime import date, datetime,timedelta
import re
import requestInformation as ri
import requests
"""_summary_
Ritorna il valore massimo dell'intensità media del vento degli ultimi 15 giorni
Da ricordare Il for ritarda l'esecuzione dell'intero programma
"""

def getMaxIntensitaVentoLastTwoWeek(centralina,toDay): #cancellare toDay
    intensitaVento=0
    toDay=date.today()
    for i in range(15):
        oldDate=toDay-timedelta(i)
        #print(oldDate)
        dataJson=ri.getInfo(centralina,oldDate,oldDate)
        #print("centralina ",centralina," valore ",float(dataJson["intensita_vento"])," data ",oldDate)
        if float(dataJson["intensita_vento"]) > intensitaVento:
            intensitaVento=float(dataJson["intensita_vento"])
    return intensitaVento

#getMaxIntensitaVentoLastTwoWeek("ITLOMBAS123456","2022-10-22")