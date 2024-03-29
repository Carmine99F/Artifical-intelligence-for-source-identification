import requestInformation as ri
import json
import config

"""_summary_
arrayCentraline : array contenente i nomi di tutte le centraline
infoCentraline: dizionario contenente per ogni nome di centralina le informazioni relative a latitudine e longitudine
La funzione per ogni centralina dato il nome ricava le info relative al pm e il vento , il dato verrà restituito in formato json
prendiamo ogni volta il pm10 e lo mettiamo un array
jsonCentraline è un dizionario con la seguente struttura {"nomeCentraline": {"info su pm e vento"}}
se esiste almeno un valore > 0 di pm10 ci facciamo restituire le coordinate delle 3 centraline più esposte al pm10
la funzione setta il valore della variabile globale contenente il valore di pm10 della centralina con maggior esposizione
"""
def getMaxCoordinates(arrayCentraline:list,infoCentraline:dict):
    jsonCentraline={}
    listPm10=[]  #questo array servirà per  controllare se tra tutti i pm10 c'è almeno un valore > 50
    for item in arrayCentraline:
        #objectInfo=ri.getInfo(item,config.data,config.data)
        objectInfo=config.dizMediaGiornaliera[item]
        if objectInfo is not None:
            listPm10.append(objectInfo["pm10"])
            jsonCentraline.update({item:objectInfo})
    if any(i>0 for i in listPm10):
        #maxPm10=list(jsonCentraline.values())[0]["pm10"]
        #maxKey=list(jsonCentraline.keys())[0]
        listPm10.sort()
        listPm10.reverse()
        config.valueMaxPm10=listPm10[0]
        firstKey=None
        secondKey=None
        thirdKey=None
        for keyCentralina,info in jsonCentraline.items():
            #print("key centraline",keyCentralina)
            if info["pm10"]==listPm10[0]:
                firstKey=keyCentralina
                config.nomeCentralina1=str(keyCentralina)
            if info["pm10"]==listPm10[1]:
                secondKey=keyCentralina
                config.nomeCentralina2=str(keyCentralina)
            if info["pm10"]==listPm10[2]:
                thirdKey=keyCentralina
                config.nomeCentralina3=str(keyCentralina)
        coordinateFirstCentralina=[infoCentraline[firstKey]["lon"],infoCentraline[firstKey]["lat"]]
        coordinateSecondCentralina=[infoCentraline[secondKey]["lon"],infoCentraline[secondKey]["lat"]]
        coordinateThirdCentralina=[infoCentraline[thirdKey]["lon"],infoCentraline[thirdKey]["lat"]]
        return coordinateFirstCentralina,coordinateSecondCentralina,coordinateThirdCentralina
    else:
        raise Exception("Non c'è nessun elemento maggiore di 0")


def getMaxCoordinates2(arrayCentraline:list,infoCentraline:dict):
    jsonCentraline={}
    listPm10=[]  #questo array servirà per  controllare se tra tutti i pm10 c'è almeno un valore > 50
    for key,item in config.dizMediaGiornaliera.items():
        listPm10.append(item["pm10"])
        jsonCentraline.update({key:item})
    if any(i>0 for i in listPm10):
        listPm10.sort()
        listPm10.reverse()
        config.valueMaxPm10=listPm10[0]
        firstKey=None
        secondKey=None
        thirdKey=None
        for keyCentralina,info in jsonCentraline.items():
            #print("key centraline",keyCentralina)
            if info["pm10"]==listPm10[0]:
                firstKey=keyCentralina
                config.nomeCentralina1=str(keyCentralina)
            if info["pm10"]==listPm10[1]:
                secondKey=keyCentralina
                config.nomeCentralina2=str(keyCentralina)
            if info["pm10"]==listPm10[2]:
                thirdKey=keyCentralina
                config.nomeCentralina3=str(keyCentralina)
        coordinateFirstCentralina=[config.dizMediaGiornaliera[firstKey]["lon"],config.dizMediaGiornaliera[firstKey]["lat"]]
        coordinateSecondCentralina=[config.dizMediaGiornaliera[secondKey]["lon"],config.dizMediaGiornaliera[secondKey]["lat"]]
        coordinateThirdCentralina=[config.dizMediaGiornaliera[thirdKey]["lon"],config.dizMediaGiornaliera[thirdKey]["lat"]]
        return coordinateFirstCentralina,coordinateSecondCentralina,coordinateThirdCentralina
    else:
        raise Exception("Non c'è nessun elemento maggiore di 0")

