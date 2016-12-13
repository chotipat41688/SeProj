def getFreefloat():
    allShare = 250000000  # ACAP
    freeFloat = 67.03
    return (allShare * freeFloat)/100

def check(list):
    if list[3] is not 0 and list[4] is 0: return 0
    else: return 1

def getSumVol(list):
    Sum = float(list[0] + list[1] + list[2] + list[3] + list[4])
    return Sum

def event(eve):
    if eve == "B":
        return 1
    else:
        return 0

def getTime(time):
    timeSplit = time.split(':')
    return timeSplit

def getDate(Date):
    dateSplit = Date.split('-')
    return dateSplit


tempBid = ",,,,,,,,,"
tempOffer = ",,,,,,,,,"
tempBidVol = 0
tempOffVol = 0
def toTemp(price,eve,vol):
    global tempBid,tempOffer,tempBidVol,tempOffVol

    sumVO = getSumVol(vol)

    if eve == 1:
        tempBid = price
        tempBidVol = sumVO
        return price+","+tempOffer+","+str(tempBidVol)+","+str(tempOffVol)
    else:
        tempOffer = price
        tempOffVol = sumVO
        return tempBid+","+price+","+str(tempBidVol)+","+str(tempOffVol)



import json
items= ["2016-12-08_FANCY_30","2016-12-09_FANCY_30"]
# items = ["2016-10-17","2016-10-18","2016-10-19","2016-10-20"]


for Date in items:

    YYYY,MM,DD = getDate(Date)

    with open("INPUT\\" +Date+".dat") as f, open("TESTWRITE\\FANCY_BOOnly" + items[0] + "to" + items[-1] + ".csv", "a") as output:         ## One file Many Day
    # with open(Date + ".dat") as f, open("TESTWRITE\\cutword_IFEC_event" + Date + ".txt", "a") as output:      ## One file One Day
        content = f.readlines()
        for line in content:
            if ('data' in line):
                jsonData = line.replace("data: ", "")
                jsonDecoded = json.loads(jsonData)
                if 'sym' in jsonDecoded.keys():
                    if jsonDecoded["sym"] == "FANCY":
                        if 'time' in jsonDecoded.keys():
                            pri = jsonDecoded["pri"]
                            if check(pri) is 0: continue

                            eve = event(jsonDecoded["sid"])
                            hh, mm, ss = getTime(jsonDecoded["time"])
                            id = jsonDecoded["id"]  ##identify number of stock
                            vol = jsonDecoded["vol"]
                            Temp = str(pri[0])+ ',' + str(pri[1])+ ',' + str(pri[2])+ ',' + str(pri[3])+ ',' + str(pri[4]) + ',' + str(vol[0])+ ',' + str(vol[1])+ ',' + str(vol[2])+ ',' + str(vol[3])+ ',' + str(vol[4])
                            a = str(id) + ',' + str(hh) + ',' + str(mm) + ',' + str(ss) + ',' + toTemp(Temp, eve,vol)
                            output.writelines(a + '\n')





