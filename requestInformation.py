from textwrap import indent
import requests
import json

def getInfo(name):
    url="https://square.sensesquare.eu:5001/download"
    #arrayInfoCentraline=[]
    #arrayCentraline=['ITCAMMON134567','ITCAMMON234567','ITCAMMON334567','ITCAMMON444567']
    #for i in range(23):
    dati={
        "apikey":"4BSFRYMNPZ0J",
        "req_type":"daily",#daily,hourly
        "zoom":5,
        "start_hour":00,
        "end_hour":23,
        "format":"json",
        "fonti":"ssq",
        "req_centr":name,
        "start_date":"2022-03-27",
        "end_date":"2022-03-27"
    }
    response=requests.post(url,data=dati)
    if response.text != "":
        arrayInfoCentraline=[]
        infoJson=json.loads(str(response.text))
        #if float(infoJson["pm10"]) > 50:
        dataJson={
                "direzione_vento":float(infoJson["direzione_vento"]),
                "gas_resistance":float(infoJson["gas_resistance"]),
                "intensita_vento":float(infoJson["intensita_vento"]),
                "pm10":float(infoJson["pm10"]),
                "pm2_5":float(infoJson["pm2_5"])
        }
            #print(dataJson)
        return dataJson
        #return None
            #arrayInfoCentraline.append(dataJson)
        #return arrayInfoCentraline
    else:
        print("Response vuota")
        return None

#print(arrayInfoCentraline)
# print(len(arrayInfoCentraline))
# print(type(arrayInfoCentraline))
# print(arrayInfoCentraline)
# strInfo="{"+str(arrayInfoCentraline)+"}"
# strInfo = strInfo.replace("\'", "\"")

# print(strInfo)
# try:
#     jsonInfo=json.loads(strInfo)
#     print(jsonInfo)
# except Exception as ex:
#     print(str(ex))
    
    
    
    
# dati={
#     "apikey":"4BSFRYMNPZ0J",
#     "req_type":"hourly",
#     "zoom":5,
#     "start_hour":0,
#     "end_hour":0,
#     "format":"json",
#     "fonti":"ssq",
#     "req_centr":"ITCAMMON134567",
#     "start_date":"2022-03-27",
#     "end_date":"2022-03-27"
# }
# response=requests.post(url,data=dati)
# print(response.text)


#print(type(response.json()))
#print(response.text)
#print(json.dumps(response.json(), indent=4))

#jsonInfo=json.dumps((response.text))
#print(response.json())

# try:
#     infoJson=json.loads(str(response.text))
#     print(infoJson)
#     print(infoJson["ID"])
#     dataJson={
#         "direzione_vento":float(infoJson["direzione_vento"]),
#         "gas_resistance":float(infoJson["gas_resistance"]),
#         "intensita_vento":float(infoJson["intensita_vento"]),
#         "pm10":float(infoJson["pm10"]),
#         "pm2_5":float(infoJson["pm2_5"])
#     }
#     print(json.dumps(dataJson,indent=4))
#     print(type(json.dumps(dataJson)))
    
    
# except Exception as ex:
#     print(str(ex))
# #print(infoJson)
