import json
import hourlyAverages as ha
import config


def getHour(i):
    orario=""
    if i >=0 and i<=9:
        orario="0"+str(i)+":00"
    else:
        orario=str(i)+":00"
    return orario

def isInRange(num,min,max):
    return min<=num<=max
 
def getRange(dirVentoC1,dirVentoC2,dirVentoC3):
    range1sx=dirVentoC1-1
    range1dx=dirVentoC1+1
    range2sx=dirVentoC2-1
    range2dx=dirVentoC2+1
    range3sx=dirVentoC3-1
    range3dx=dirVentoC3+1
    arrayRange=[]
    if dirVentoC1!=0:
        range1=[float(range1sx),float(range1dx+1)]
        arrayRange.append(range1)
    if dirVentoC2!=0:
        range2=[float(range2sx),float(range2dx+1)]
        arrayRange.append(range2)
    if dirVentoC3!=0:
        range3=[float(range3sx),float(range3dx+1)]
        arrayRange.append(range3)
    #arrayRange=[range1,range2,range3]
    count1=0
    count2=0
    count3=0
    #print(num1,num2,num3)
    arrayCount=[]
    for itemRange in arrayRange:
        if isInRange(dirVentoC1,itemRange[0],itemRange[1]):
            count1=count1+1
        if isInRange(dirVentoC2,itemRange[0],itemRange[1]):
            count2=count2+1
        if isInRange(dirVentoC3,itemRange[0],itemRange[1]):
            count3=count3+1
    arrayCount=[count1,count2,count3]
    while 0 in arrayCount:
        arrayCount.remove(0)
    #print(arrayCount) #print(set(arrayCount))  #print(len(set(arrayCount)))     
    if(len(arrayCount)==3):
        if(len(set(arrayCount))==1):
            #print("100")
            return 100
        if(len(set(arrayCount))==2):
            return 66
        if(len(set(arrayCount))==3):
            return 33
        
    if(len(arrayCount)==2):
        if(len(set(arrayCount))==1):
            return 66
        if(len(set(arrayCount))==2):
            return 33

    
    """   
    if count1==count2 and count1==count3:
        return 100
    if count1!=count2 and count2!=count3 and count1!=count3:
        return 33
    if (count1==count2 and count1!=count3) or (count2==count3 and count2!=count1) or(count1==count3 and count1!=count2):
        return 66
    """
               


def dailyPercentage(nomiCentraline: list):
    probabilita:float 
   
    dizC1=config.dizMediaOraria[config.nomeCentralina1]
    dizC2=config.dizMediaOraria[config.nomeCentralina2]
    dizeC3=config.dizMediaOraria[config.nomeCentralina3]
    #print(json.dumps(dizC1,indent=3))
    n=0
    for i in range(24):
        orario=getHour(i)
        if orario  in dizC1.keys() and orario in dizC2.keys() and orario in dizeC3.keys() :
            
            direzioneC1=float(dizC1[orario]["direzione"])
            #Questi due definiscono il range di C1, 
            #bisogna controllare se anche la direzione delle altre due centraline rientra nello stesso range
            direzioneC2=float(dizC2[orario]["direzione"])
            direzioneC3=float(dizeC3[orario]["direzione"])
            probabilita=getRange(direzioneC1,direzioneC2,direzioneC3)
            #print("probabilità " ,probabilita)
            n2=0
            if probabilita>=66:
                n=n+1
            if probabilita==33:
                n2=n2+1
    #print("n ",n)
    pg=(n/24)*100
    if n2>6:
        print("Alta probabilità")
    print("Numero di ore con proababilià >= 66",n)
    #print("pg ",pg)
    config.probDay=pg
    return pg

       
#dailyPercentage('ITLOMBAS123456','ITLOMBAS234567', 'ITLOMBAS334567')
