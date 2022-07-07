import requestInformation as ri
import json

"""_summary_
arrayCentraline : array contenente i nomi di tutte le centraline
infoCentraline: dizionario contenente per ogni nome di centralina le informazioni relative a latitudine e longitudine
La funzione per ogni centralina dato il nome ricava le info relative al pm e il vento , il dato verrà restituito in formato json
prendiamo ogni volta il pm10 e lo mettiamo un array
jsonCentraline è un dizionario con la seguente struttura {"nomeCentraline": {"info su pm e vento"}}
se esiste almeno un valore > 50 di pm10 ci facciamo restituire le coordinate della centralina più esposta al pm10
"""
def getMaxCoordinates(arrayCentraline:list,infoCentraline:dict):
    jsonCentraline={}
    listPm10=[]
    for item in arrayCentraline:
        objectInfo=ri.getInfo(item)
        if objectInfo is not None:
            listPm10.append(objectInfo["pm10"])
            jsonCentraline.update({item:objectInfo})
    if any(i>50 for i in listPm10):
        print("C'è un elemento maggiore di 50")
        maxPm10=list(jsonCentraline.values())[0]["pm10"]
        maxKey=list(jsonCentraline.keys())[0]
        for keyCentraline,objectInfo in jsonCentraline.items():
            if(objectInfo["pm10"])>maxPm10:
                maxPm10=objectInfo["pm10"]
                maxKey=keyCentraline
        coordinateMax=[infoCentraline[maxKey]["lon"],infoCentraline[maxKey]["lat"]]
        return coordinateMax
    else:
        print("Non c'è nessun elemento maggiore di 50")
        return None

    