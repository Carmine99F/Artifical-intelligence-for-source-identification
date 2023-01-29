
import requests
import json
import config
import math


coefficienteClass={
    1:{
        "a":0.32,
        "b":0.0004,
        "c":-0.5,
        "d":0.24,
        "e":0.001,
        "f":0.5
    },
    2:{
        "a":0.16,
        "b":0.0004,
        "c":-0.5,
        "d":0.14,
        "e":0.0003,
        "f":-0.5
    },
    3:{
        "a":0.11,
        "b":0.0004,
        "c":-0.5,
        "d":0.08,
        "e":0.000015,
        "f":-0.5
    }
}

def getConcentrazioneSorgente(intensitaVento,orario,dp):
    #print("dentro getConcentrazioneSorgente")
    intensitaVento=float(intensitaVento)

    classe=None
    if (orario >=18 and orario <=24) or (orario>=0 and orario <=6): 
        classe=1
    if intensitaVento>=6:
        classe=1
    if intensitaVento>=3 and intensitaVento<=5.99:
        classe=2
    if intensitaVento<2.99:
        classe=3
    #print("classe ", classe)
    a=coefficienteClass[classe]["a"]
    b=coefficienteClass[classe]["b"]
    c=coefficienteClass[classe]["d"]
    d=coefficienteClass[classe]["d"]
    e=coefficienteClass[classe]["e"]
    f=coefficienteClass[classe]["f"]
    sigmaY=a*dp*((1+ (b*dp))**c)
    sigmaZ=d*dp*((1+(e*dp))**f)
    
    S=math.pow(10,3)
    p=1.25*(math.pow(10,3))
    if intensitaVento!=0:
        concentrazioneSorgente=(S*p)/(2*intensitaVento*3.14*sigmaY*sigmaZ)
        return concentrazioneSorgente
    return 0

def getDP(valuePm10):
    S=math.pow(10,3)
    p=1.25*(math.pow(10,3))
    sp=S*p
    div=sp/valuePm10
    dp=int(math.sqrt((div)))
    return int(dp)


"""
restituice un json con le info sulle centraline rispetto ai valori della media oraria 
"""
def getInfo(idCentraline: list):
    #print(sys._getframe(1).f_code.co_name)
    url="https://square.sensesquare.eu:5001/download"
    dictMaxSensor={
            #nameCentralina:{},
            #nameCentralina2:{},
            #nameCentralina3:{},
            #nameCentralina4:{}           
        }
    for name in idCentraline:
        #dictMaxSensor.update({str(name):{}})
        dati={
            "apikey":"WDBNX4IUF66C",
            "req_type":"hourly",#daily,hourly
            "zoom":5,
            "start_hour":00,
            "end_hour":23,
            "format":"json",
            "fonti":"['ssq']",
            "req_centr":name,
            "start_date":config.data,
            "end_date":config.data
        }
        
        response=requests.post(url,data=dati)
        if response.status_code==200:
            if response.text != "":
                dictMaxSensor.update({str(name):{}})
                #print(response.text)
                arrayInfo=response.text.split("}")
                del arrayInfo[-1]
                ora=0
                for info in arrayInfo:
                    ora=ora+1
                    if ora-1 <10:
                        hours="0"+str(ora-1)+":00"
                    elif ora >=10:
                        hours=str(ora-1)+":00"
                    info=info+"}"       
                    diz=json.loads(info)
                    intensita_vento=0
                    direzione_vento=0
                    dp=getDP(float(diz["pm10"]))
                    intensita_vento=0
                    direzione_vento=0
                    if "intensita_vento" in diz.keys():
                        intensita_vento=diz["intensita_vento"]
                    if "direzione_vento" in diz.keys():
                        direzione_vento=diz["direzione_vento"]
                    #print("prima della chiamata ",intensita_vento,ora,dp)
                    concentrazioneSorgente=getConcentrazioneSorgente(intensita_vento,ora,dp)
                    probabilitaOraria:float
                    dictMaxSensor[name].update({
                            hours:{
                                "pm10":diz["pm10"],
                                "direzione":direzione_vento,
                                "dp":dp,
                                "concentrazioneSorgente":concentrazioneSorgente
                            }
                        })
        else:
            raise Exception("Richiesta fallita , status code ",response.status_code)
    config.dizMediaOraria=dictMaxSensor           
    #print(json.dumps(dictMaxSensor,indent=2))
    
#getInfo(config.arrayNomiCentraline)          



