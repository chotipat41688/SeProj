symbols = ["FANCY"]

# items= ["2016-12-09_FANCY_30"]
# items= ["2016-12-09_FANCY_30","2016-10-13","2016-10-14","2016-11-11","2016-11-14","2016-11-15","2016-11-30","2016-12-14_30","2016-12-15_30"]

items= [ "2016-12-19"]




def getFreefloat():
    allShare = 250000000  # ACAP
    freeFloat = 67.03
    return (allShare * freeFloat)/100

def check(list):
    if list[1] is not 0 and list[2] is not 0 and list[4] is 0: return 0
    else: return 1

def getSumVol(list):
    Sum = list[0] + list[1] + list[2] + list[3] + list[4]
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


def toTemp(price, vol, eve, symbol):
    sumVO = getSumVol(vol)

    if eve == 1:
        tempBid[symbol] = price + vol
        tempBidVol[symbol] = [sumVO]
        return price + vol + tempOffer[symbol] + tempBidVol[symbol] + tempOffVol[symbol]
    else:
        tempOffer[symbol] = price + vol
        tempOffVol[symbol] = [sumVO]
        return tempBid[symbol] + price + vol + tempBidVol[symbol] + tempOffVol[symbol]


import json
import csv
import time

t0 = time.time()

tempBid = dict()
tempOffer = dict()
tempBidVol = dict()
tempOffVol = dict()
tempAll = dict()

for symbol in symbols:
    tempBid[symbol] = [None, None, None, None, None, None, None, None, None, None]
    tempOffer[symbol] = [None, None, None, None, None, None, None, None, None, None]

for symbol in symbols:
    tempBidVol[symbol] = []
    tempOffVol[symbol] = []


ref_files = [open("TESTWRITE\\List\\" + Symbol + ".csv", "a") for Symbol in symbols]

for Date in items:

    YYYY,MM,DD = getDate(Date)

    with open("INPUT\\" +Date+".dat") as f:
        with open("TESTWRITE\\ma1" + items[0] + "to" + items[-1] + ".csv", "a") as output:         ## One file Many Day


    # with open(Date + ".dat") as f, open("TESTWRITE\\cutword_IFEC_event" + Date + ".txt", "a") as output:      ## One file One Day
            content = f.readlines()
            for line in content:
                if ('data' in line):
                    try:
                        jsonData = line.replace("data: ", "")
                        jsonDecoded = json.loads(jsonData)
                    except ValueError:
                        print Date, jsonData
                        continue
                    if 'sym' in jsonDecoded.keys():
                        if jsonDecoded["sym"] in symbols:
                            if 'time' in jsonDecoded.keys():
                                pri = jsonDecoded["pri"]
                                if check(pri) is 0: continue

                                sym = jsonDecoded["sym"]
                                eve = event(jsonDecoded["sid"])
                                hh, mm, ss = getTime(jsonDecoded["time"])
                                id = jsonDecoded["id"]  ##identify number of stock
                                vol = jsonDecoded["vol"]

                                a = [id] + [hh] + [mm] + [ss] + toTemp(pri, vol, eve, sym)

                                wr = csv.writer(ref_files[symbols.index(sym)], lineterminator='\n')
                                wr.writerow(a)










t1 = time.time()


total = t1-t0

print total

