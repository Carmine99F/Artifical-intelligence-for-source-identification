import hourlyAverages as ha
import config
import numpy as np

def getHour(i):
    orario=""
    if i >=0 and i<=9:
        orario="0"+str(i)+":00"
    else:
        orario=str(i)+":00"
    return orario

"""    
def getRange(num1,num2,num3,range1sx,range1dx,range2sx,range2dx,range3sx,range3dx):
    range1sx=int(range1sx)
    range1dx=int(range1dx+1)
    range2sx=int(range2sx)
    range2dx=int(range2dx+1)
    range3sx=int(range3sx)
    range3dx=int(range3dx+1)
 
    # print("num1",(num1))
    # print("num2",num2)
    # print("num3",num3)
    # print(range1sx,range1dx)
    # print(range2sx,range2dx)
    # print(range3sx,range3dx)
    
    if num1 in range(range1sx,range1dx) and num2 in range(range1sx,range1dx+1) and num3 in range(range1sx,range1dx+1):
        print("prob 100")
    if num1 in range(range2sx,range2dx) and num2 in range(range2sx,range2dx) and num3 in range(range2sx,range2dx):
        print("100")
    if num1 in range(range3sx,range3dx) and num2 in range(range3sx,range3dx) and num3 in range(range3sx,range3dx):
        print("100")
        
    if num1 in range(range1sx,range1dx) and num2 in range(range1sx,range1dx) and num3 not in range(range1sx,range1dx):
        print("66")
    if num1 not  in range(range1sx,range1dx) and num2 in range(range1sx,range1dx) and num3 not in range(range1sx,range1dx):
        print("66")
    if num1 in range(range1sx,range1dx) and num2 not in range(range1sx,range1dx) and num3 in range(range1sx,range1dx):
        print("66")
    
    count1=0
    count2=0
    count3=0
    
    
    arrayRange=[ [range1sx,range1dx],[range1sx,range2dx],[range3sx,range3dx]]
    for array in arrayRange:
        if num1 in range(array[0],array[1]):
            count1=count1+1
        if num2 in range(array[0],array[1]):
            count2=count2+1
        if num1 in range(array[0],array[1]):
            count3=count3+1
    print("count 1" ,count1)
    print("count 2" ,count2)
    print("count 3" ,count3)

"""
    
    
"""
def getRange(num1,num2,num3,range1sx,range1dx,range2sx,range2dx,range3sx,range3dx):
    range1=range(float(range1sx),float(range1dx+1),1)
    range2=range(float(range2sx),float(range2dx+1),1)
    range3=range(float(range3sx),float(range3dx+1),1)
    print(range1)
    print(range2)
    print(range3)
    arrayRange=[range1,range2,range3]
    count1=0
    count2=0
    count3=0
    #print(num1,num2,num3)
    for itemRange in arrayRange:
        if num1 in itemRange:
            count1=count1+1
        if num2 in itemRange:
            count2=count2+1
        if num3 in itemRange:
            count3=count3+1
    if count1==count2 and count1==count3 and count1==count2:
         return 100
    if count1!=count2 and count2!=count3 and count1!=count3:
        return 33
    if (count1==count2 and count1!=count3) or (count2==count3 and count2!=count1) or(count1==count3 and count1!=count2):
        return 66       
"""


def isInRange(num,min,max):
    return min<=num<=max
 
def getRange2(dirVentoC1,dirVentoC2,dirVentoC3,
              range1sx,range1dx,range2sx,range2dx,range3sx,range3dx):
    
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
            #print(dirVentoC1," è compreso tra ", itemRange[0], " e ",itemRange[1])
            count1=count1+1
        if isInRange(dirVentoC2,itemRange[0],itemRange[1]):
            #print(dirVentoC2," è compreso tra ", itemRange[0], " e ",itemRange[1])
            count2=count2+1
        if isInRange(dirVentoC3,itemRange[0],itemRange[1]):
            #print(dirVentoC3," è compreso tra ", itemRange[0], " e ",itemRange[1])
            count3=count3+1
    arrayCount=[count1,count2,count3]
    while 0 in arrayCount:
        arrayCount.remove(0)
    print(arrayCount)
    print(set(arrayCount))
    print(len(set(arrayCount)))     
    
    
    if(len(arrayCount)==3):
        if(len(set(arrayCount))==1):
            print("100")
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
               
# def getRange3(dirVentoC1,dirVentoC2,dirVentoC3,
#               range1sx,range1dx,range2sx,range2dx,range3sx,range3dx):
#     if dirVentoC1==0 or dirVentoC2==0 or dirVentoC3==0:
#         print("uno dei 3 è 0")
#         print(dirVentoC1,dirVentoC2,dirVentoC3)
#     arrayRange=[]
#     arrayDirectionCentraline=[]
#     if dirVentoC1!=0:
#         range1=[float(range1sx),float(range1dx+1)]
#         arrayRange.append(range1)
#         arrayDirectionCentraline.append(dirVentoC1)
#     if dirVentoC2!=0:
#         range2=[float(range2sx),float(range2dx+1)]
#         arrayRange.append(range2)
#         arrayDirectionCentraline.append(dirVentoC2)

#     if dirVentoC3!=0:
#         range3=[float(range3sx),float(range3dx+1)]
#         arrayRange.append(range3)
#         arrayDirectionCentraline.append(dirVentoC3)

#     #arrayRange=[range1,range2,range3]
#     count1=0
#     count2=0
#     count3=0
#     arrayCount=[]
#     #print(num1,num2,num3)
    
#     for itemRange in arrayRange:
#         for direction in arrayDirectionCentraline:
#             if isInRange(direction,itemRange[0],itemRange[1]):
#                 pass
#     """
#     for itemRange in arrayRange:
#         if isInRange(dirVentoC1,itemRange[0],itemRange[1]):
#             count1=count1+1
#         if isInRange(dirVentoC2,itemRange[0],itemRange[1]):
#             count2=count2+1
#         if isInRange(dirVentoC3,itemRange[0],itemRange[1]):
#             count3=count3+1
#     """
#     if count1==count2 and count1==count3:
#         return 100
#     if count1!=count2 and count2!=count3 and count1!=count3:
#         return 33
#     if (count1==count2 and count1!=count3) or (count2==count3 and count2!=count1) or(count1==count3 and count1!=count2):
#         return 66           

def dailyPercentage(nameC1,nameC2,nameC3):
    probabilita=None
    dizC1=ha.getInfo(nameC1,config.data,config.data)
    dizC2=ha.getInfo(nameC2,config.data,config.data)
    dizeC3=ha.getInfo(nameC3,config.data,config.data)
    n=0
    for i in range(24):
        orario=getHour(i)
        direzioneC1=float(dizC1[orario]["direzione"])
        #Questi due definiscono il range di C1, 
        #bisogna controllare se anche la direzione delle altre due centraline rientra nello stesso range
        sx1=direzioneC1-1
        dx1=direzioneC1+1
        direzioneC2=float(dizC2[orario]["direzione"])
        sx2=direzioneC2-1
        dx2=direzioneC2+1
        direzioneC3=float(dizeC3[orario]["direzione"])
        sx3=direzioneC3-1
        dx3=direzioneC3+1
        probabilita=getRange2(direzioneC1,direzioneC2,direzioneC3,sx1,dx1,sx2,dx2,sx3,dx3)
        n2=0
        if probabilita>=66:
            n=n+1
        if probabilita==33:
            n2=n2+1
    print("n ",n)
    pg=(n/24)*100
    if n2>6:
        print("Alta probabilità")
    print("pg ",pg)
    return pg

       
dailyPercentage('ITLOMBAS123456','ITLOMBAS234567', 'ITLOMBAS334567')