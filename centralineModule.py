import requestInformation as ri
import json

"""_summary_
arrayCentraline : array contenente i nomi di tutte le centraline
infoCentraline: dizionario contenente per ogni nome di centralina le informazioni relative a latitudine e longitudine
La funzione per ogni centralina dato il nome ricava le info relative al pm e il vento , il dato verrà restituito in formato json
prendiamo ogni volta il pm10 e lo mettiamo un array
jsonCentraline è un dizionario con la seguente struttura {"nomeCentraline": {"info su pm e vento"}}
se esiste almeno un valore > 50 di pm10 ci facciamo restituire le coordinate delle 3 centraline più esposte al pm10

"""
def getMaxCoordinates(arrayCentraline:list,infoCentraline:dict):
    jsonCentraline={}
    listPm10=[]  #questo array servirà per  controllare se tra tutti i pm10 c'è almeno un valore > 50
    for item in arrayCentraline:
        objectInfo=ri.getInfo(item)
        if objectInfo is not None:
            listPm10.append(objectInfo["pm10"])
            jsonCentraline.update({item:objectInfo})
            print(jsonCentraline)
    if any(i>0 for i in listPm10):
        print("C'è un elemento maggiore di 50")
        maxPm10=list(jsonCentraline.values())[0]["pm10"]
        maxKey=list(jsonCentraline.keys())[0]
        listPm10.sort()
        listPm10.reverse()
        firstKey=None
        secondKey=None
        thirdKey=None
        for keyCentralina,info in jsonCentraline.items():
            if info["pm10"]==listPm10[0]:
                firstKey=keyCentralina
            if info["pm10"]==listPm10[1]:
                secondKey=keyCentralina
            if info["pm10"]==listPm10[2]:
                thirdKey=keyCentralina
        coordinateFirstCentralina=[infoCentraline[firstKey]["lon"],infoCentraline[firstKey]["lat"]]
        coordinateSecondCentralina=[infoCentraline[secondKey]["lon"],infoCentraline[secondKey]["lat"]]
        coordinateThirdCentralina=[infoCentraline[thirdKey]["lon"],infoCentraline[thirdKey]["lat"]]
        return coordinateFirstCentralina,coordinateSecondCentralina,coordinateThirdCentralina
    else:
        print("Non c'è nessun elemento maggiore di 50")
        return None,None,None


