import json
import csv
import time
from datetime import datetime, timedelta
from numpy import array
import numpy as np

import MySQLdb
db = MySQLdb.connect("localhost","root","Qwer41688","dballstock")
cursor = db.cursor()

# symbols = ["JAS","JAS-W3","DTAC"]
# items = ["2017-01-24","2017-01-25"]
# items= ["2016-12-09_FANCY_30"]
# items= ["2016-12-09_FANCY_30","2016-10-13","2016-10-14","2016-11-11","2016-11-14","2016-11-15","2016-11-30","2016-12-14_30","2016-12-15_30"]
# items= ["Sample"]
symbols = ["OTO", "HPT", "AMANAH"]
items = ["2017-02-14", "2017-02-15"]

def getFreefloat():
    allShare = 250000000  # ACAP
    freeFloat = 67.03
    return (allShare * freeFloat)/100

def check(list):
    if list[1] is not 0 and list[2] is not 0 and list[4] is 0: return 0
    else: return 1

def getSumVol(list):
    # Sum = list[0] + list[1] + list[2] + list[3] + list[4]
    Sum = np.sum(list)
    return Sum

def event(eve):
    if eve == "B":
        return 1
    elif eve == "S":
        return 0
    else:
        return 5

def getTime(time):
    timeSplit = time.split(':')
    return timeSplit

def getDate(Date):
    dateSplit = Date.split('-')
    return dateSplit


def Timestamp2Datetime(Timestamp):
    Datetime = datetime.fromtimestamp(Timestamp-25200).strftime('%Y-%m-%d-%H-%M-%S')
    # print Datetime
    return Datetime

def Datetime2Timestamp(dt, epoch=datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) // 10**6


def toTemp(price, vol, eve, symbol):
    sumVO = getSumVol(vol)
    compareBid1[symbol] = tempBid[symbol][5]
    compareOff1[symbol] = tempOffer[symbol][5]


    if eve == 1:

        tempBid[symbol] = price + vol

        difBO[symbol] = sumVO - tempBidVol[symbol]

        if difBO[symbol] <= -1000000:
            volBO[symbol] = -4
        elif -1000000 < difBO[symbol] <= -500000:
            volBO[symbol] = -3
        elif -500000 < difBO[symbol] <= -100000:
            volBO[symbol] = -2
        elif -100000 < difBO[symbol] <= -100:
            volBO[symbol] = -1
        elif -100 < difBO[symbol] <= 100000:
            volBO[symbol] = 1
        elif 100000 < difBO[symbol] <= 500000:
            volBO[symbol] = 2
        elif 500000 < difBO[symbol] <= -1000000:
            volBO[symbol] = 3
        elif difBO[symbol] > 1000000:
            volBO[symbol] = 4

        tempBidVol[symbol] = sumVO
        return price + vol + tempOffer[symbol] + [tempBidVol[symbol]] + [tempOffVol[symbol]]
    else:

        tempOffer[symbol] = price + vol

        difBO[symbol] = sumVO - tempOffVol[symbol]

        if difBO[symbol] <= -1000000:
            volBO[symbol] = -40
        elif -1000000 < difBO[symbol] <= -500000:
            volBO[symbol] = -30
        elif -500000 < difBO[symbol] <= -100000:
            volBO[symbol] = -20
        elif -100000 < difBO[symbol] <= -100:
            volBO[symbol] = -10
        elif -100 < difBO[symbol] <= 100000:
            volBO[symbol] = 10
        elif 100000 < difBO[symbol] <= 500000:
            volBO[symbol] = 20
        elif 500000 < difBO[symbol] <= -1000000:
            volBO[symbol] = 30
        elif difBO[symbol] > 1000000:
            volBO[symbol] = 40

        tempOffVol[symbol] = sumVO
        return tempBid[symbol] + price + vol + [tempBidVol[symbol]] + [tempOffVol[symbol]]



def checkTimestamp(timestamp,symbol):
    if timestamp < tempTimestamp[symbol]:
        return tempTimestamp[symbol],1
    else:
        tempTimestamp[symbol] = timestamp
        return timestamp,0










def getSpread(x):
    ''' x<2         0.01    0
        2<=x<5       0.02    1
        5<=x<10      0.05    2
        10<=x<25     0.1     3
        25<=x<100    0.25    4
        100<=x<200   0.5     5
        200<=x<400   1.0     6
        x>=400       2.0     7
    '''
    if x < 200:
        return 0, 1, 200
    elif 200 <= x < 500:
        return 1, .5, 500
    elif 500 <= x < 1000:
        return 2, .2, 1000
    elif 1000 <= x < 2500:
        return 3, .1, 2500
    elif 2500 <= x < 10000:
        return 4, .04, 10000
    elif 10000 <= x < 20000:
        return 5, .02, 20000
    elif 20000 <= x < 40000:
        return 6, .01, 40000
    else:
        return 7, .005, 40000

def getDifSpread(x1, x2):
    a1, t1, z1 = getSpread(x1)
    a2, t2, z2 = getSpread(x2)
    if a1 == a2:
        Dif = (x2 - x1) * t1
    elif a2 > a1:
        Dif = ((x2 - z1) * t2) + ((z1 - x1) * t1)
    else:
        Dif = -(((x1 - z2) * t1) + ((z2 - x2) * t2))
    return int(Dif)



def calmoney(pbid0,pbid1,pbid2,pbid3,pbid4,vbid0,vbid1,vbid2,vbid3,vbid4):
    money = ((pbid0*vbid0)+(pbid1*vbid1)+(pbid2*vbid2)+(pbid3*vbid3)+(pbid4*vbid4))/100
    return money







t0 = time.time()

idSymbol = dict()
tempBid = dict()
tempOffer = dict()
tempBidVol = dict()
tempOffVol = dict()
tempAll = dict()
priATO = dict()
volATO = dict()
tempTimestamp = dict()
marketStatus = dict()
forTemp = dict()
clearNoise = dict()

sumOrder = dict()
countOrder = dict()

lastPrice = dict()
prior = dict()
highPrice = dict()
lowPrice = dict()
avgPrice = dict()
tradeVol = dict()
buyVol = dict()
sellVol = dict()
auctVol = dict()

spread = dict()
count100k = dict()
difBO = dict()

tf30 = dict()
volBO = dict()
typeBO = dict()
compareBid1 = dict()
compareOff1 = dict()


allbidmoney = dict()
sidetransac = dict()


for symbol in symbols:
    # tempBid[symbol] = [None, None, None, None, None, None, None, None, None, None]
    # tempOffer[symbol] = [None, None, None, None, None, None, None, None, None, None]
    tempBid[symbol] = [0,0,0,0,0,0,0,0,0,0]
    tempOffer[symbol] = [0,0,0,0,0,0,0,0,0,0]
    # forTemp[symbol] = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]

    priATO[symbol] = 0
    volATO[symbol] = 0
    tempTimestamp[symbol] = 0
    marketStatus[symbol] = 0
    clearNoise[symbol] = 0
    idSymbol[symbol] = 0

    sumOrder[symbol] = 0
    countOrder[symbol] = 0

    lastPrice[symbol] = 0
    prior[symbol] = 0
    highPrice[symbol] = 0
    lowPrice[symbol] = 0
    avgPrice[symbol] = 0
    tradeVol[symbol] = 0
    buyVol[symbol] = 0
    sellVol[symbol] = 0
    auctVol[symbol] = 0

    spread[symbol] = 0
    count100k[symbol] = 0
    difBO[symbol] =0
    tf30[symbol] = 0
    volBO[symbol] = 0
    typeBO[symbol] = 0

    tempBidVol[symbol] = 0
    tempOffVol[symbol] = 0
    compareBid1[symbol] = 0
    compareOff1[symbol] = 0

    allbidmoney[symbol] = 0
    sidetransac[symbol] = 0


for symbol in symbols:
    forTemp[symbol] = []


ref_files = [open("TESTWRITE\\List\\" + Symbol + ".csv", "a") for Symbol in symbols]
ref_files2 = [open("TESTWRITE\\Listato\\" + Symbol + ".csv", "a") for Symbol in symbols]

for Date in items:

    YYYY,MM,DD = getDate(Date)

    YYYY = int(YYYY)
    MM = int(MM)
    DD = int(DD)


    with open("INPUT\\" +Date+".dat") as f:
        with open("TESTWRITE\\ma1" + items[0] + "to" + items[-1] + ".csv", "a") as output:         ## One file Many Day


    # with open(Date + ".dat") as f, open("TESTWRITE\\cutword_IFEC_event" + Date + ".txt", "a") as output:      ## One file One Day
            content = f.readlines()
            for line in content:
                if 'data' in line:
                    try:
                        jsonData = line.replace("data: ", "")
                        jsonDecoded = json.loads(jsonData)
                    except ValueError:
                        # print Date, jsonData
                        continue

                    if 'sym' in jsonDecoded.keys():
                        sym = jsonDecoded["sym"]
                        if sym in symbols:
                            if 'isf' in jsonDecoded.keys():

                                """
                                ("isf" is about Proj.Price and Proj.Vol @ ATO/ATC)
                                'isf': 'T' is Confirmed Proj. and use data before this state  (use latest 'isf': 'F')
                                'isf': 'T' tag is use to find time that ATO/ATC is take action.
                                """

                                pri = jsonDecoded["pri"]  # price
                                priATO[sym] = pri

                                tim = jsonDecoded["tim"]    #time
                                HH, mm, SS = getTime(jsonDecoded["tim"])            ###
                                HH = int(HH)
                                mm = int(mm)
                                SS = int(SS)
                                Timestamp = Datetime2Timestamp(datetime(YYYY, MM, DD, HH, mm, SS))  ###
                                Timestamp = checkTimestamp(Timestamp,sym)

                                vol = jsonDecoded["vol"]  # volume
                                volATO[sym] = vol

                                op1 = jsonDecoded["op1"]  # open1
                                op2 = jsonDecoded["op2"]  # open2

                                isf = jsonDecoded["isf"]
                                if isf == 'F':
                                    marketStatus[sym] = 0   #Pre-Open1
                                    if HH == 14:
                                        marketStatus[sym] = 2   #Pre-Open2
                                    if HH == 16:
                                        marketStatus[sym] = 3  # Pre-Open2

                                elif isf == 'T':
                                    marketStatus[sym] = 1   #Open
                                    clearNoise[sym] = Timestamp[0]

                                    if HH == 16 and mm >30:
                                        marketStatus[sym] = 4   #Pre-Close
                                else:
                                    marketStatus[sym] = 5
                                    print "Unknown status"


                                # a = [marketStatus[sym]] + [None] +  [Timestamp[0]]+ [Timestamp[1]] + [Date] + [tim] + [pri] + [vol] + [op1] + [op2]
                                # wr = csv.writer(ref_files[symbols.index(sym)], lineterminator='\n')
                                # wr.writerow(a)




                                # isf = jsonDecoded["isf"]    #isFinal? True or False
                                # if pri != 0 and vol != 0:
                                #     a = (str(id) + ',5,'  + str(hh) + ',' + str(mm) + ',' + str(ss) + ',' + str(pri) + ',' + str(vol) + ',' + str(op1) + ',' + str(op2)) + ',' + str(totalVol)
                                #     output.writelines(a + '\n')

                            elif 'time' in jsonDecoded.keys():
                                pri = jsonDecoded["pri"]
                                if check(pri) is 0:
                                    continue

                                eve = event(jsonDecoded["sid"])

                                tim = jsonDecoded["time"]
                                HH, mm, SS = getTime(jsonDecoded["time"])  ###
                                HH = int(HH)
                                mm = int(mm)
                                SS = int(SS)

                                Timestamp = Datetime2Timestamp(datetime(YYYY, MM, DD, HH, mm, SS))  ###
                                Timestamp = checkTimestamp(Timestamp,sym)

                                tempY, tempM, tempD, HH, mm, SS = getDate(Timestamp2Datetime(Timestamp[0]))
                                HH = int(HH)
                                mm = int(mm)
                                SS = int(SS)



                                ids = jsonDecoded["id"]  ##identify number of stock
                                idSymbol[sym] = ids

                                vol = jsonDecoded["vol"]

                                # if jsonDecoded["sid"] == 'S':
                                #     side = 1  # Fill Offer
                                # elif jsonDecoded["sid"] == 'B':
                                #     side = 0  # Fill Bid
                                # else:
                                #     side = 3

                                side = event(jsonDecoded["sid"])

                                bidOffer = toTemp(pri, vol, eve, sym)


                                allbidmoney[sym] = calmoney(bidOffer[0],bidOffer[1],bidOffer[2],bidOffer[3],bidOffer[4],bidOffer[5],bidOffer[6],bidOffer[7],bidOffer[8],bidOffer[9])




                                if bidOffer[0] == 0 and marketStatus[sym] != 1:
                                    bidOffer[0] = priATO[sym]
                                if bidOffer[10] == 0 and marketStatus[sym] != 1:
                                    bidOffer[10] = priATO[sym]

                                if marketStatus[sym] == 1:
                                    spread[sym] = getDifSpread(prior[sym],bidOffer[0])

                                    if HH < 10:
                                        tf30[sym] = 0
                                    elif HH == 10 and mm < 30:
                                        tf30[sym] = 1
                                    elif HH == 10 and mm >= 30:
                                        tf30[sym] = 2
                                    elif HH == 11 and mm < 30:
                                        tf30[sym] = 3
                                    elif HH == 11 and mm >= 30:
                                        tf30[sym] = 4
                                    elif HH == 12 and mm <= 30:
                                        tf30[sym] = 5
                                    elif HH == 14 and mm < 30:
                                        tf30[sym] = 6
                                    elif HH == 14 and mm >= 30:
                                        tf30[sym] = 7
                                    elif HH == 15 and mm < 30:
                                        tf30[sym] = 8
                                    elif HH == 15 and mm >= 30:
                                        tf30[sym] = 9
                                    elif HH == 16 and mm <= 30:
                                        tf30[sym] = 10


                                # if side == 1:   #B(Bid)=1, S(Offer)=0
                                #     if sumOrder[sym] == 0:
                                #         if bidOffer[5] != tempBid[sym][5]:
                                #             typeBO = 0
                                #         else:
                                #
                                # if bidOffer[15] != tempOffer[sym][5]:
                                if sumOrder[sym] != 0:
                                    volBO[sym] = sumOrder[sym]
                                    # typeBO[sym] = side
                                    if sidetransac[sym] == 0:
                                        typeBO[sym] = 'Sell'
                                    else:
                                        typeBO[sym] = 'Buy'
                                else:
                                    if side == 1:
                                        if compareBid1[sym] == bidOffer[5]:
                                            typeBO[sym] = 'Bid Not slot 0'
                                        else:
                                            typeBO[sym] = 'Bid is slot 0'
                                    else:
                                        if compareOff1[sym] == bidOffer[15]:
                                            typeBO[sym] = 'Offer Not slot 0'
                                        else:
                                            typeBO[sym] = 'Offer is slot 0'

                                # a = [marketStatus[sym]] + [id] + [Timestamp[0]]+ [Timestamp[1]] + [side]+ [Date] + [tim] + bidOffer

                                # forTemp[sym] = [Date] + [tim] + [idSymbol[sym]] + [marketStatus[sym]] + [Timestamp[0]]+ [Timestamp[1]] + [side] + bidOffer + \
                                #                [volATO[sym]] + [sumOrder[sym]] + [countOrder[sym]] + \
                                #                [tradeVol[sym]] + [lastPrice[sym]] + [prior[sym]] + [highPrice[sym]] + [lowPrice[sym]] + [avgPrice[sym]] + \
                                #                [gain[sym]] + [count100k[sym]] + [buyVol[sym]] + [sellVol[sym]] + [auctVol[sym]]



                                forTemp[sym] = [tf30[sym]] + [Date] + [tim] + [HH] + [mm] + [SS] + [idSymbol[sym]]  + [Timestamp[0]] + [Timestamp[1]] + bidOffer + \
                                               [difBO[sym]] + [volBO[sym]] + [typeBO[sym]] + [allbidmoney[sym]] +[compareOff1[sym]] + [bidOffer[15]] + [side] + [sumOrder[sym]] + [countOrder[sym]] + \
                                               [tradeVol[sym]] + [lastPrice[sym]] + [prior[sym]] + [highPrice[sym]] + [lowPrice[sym]] + [avgPrice[sym]] + \
                                               [spread[sym]] + [count100k[sym]] + [buyVol[sym]] + [sellVol[sym]] + [auctVol[sym]]


                                if clearNoise[sym] == Timestamp[0]:
                                    continue

                                if HH == 9 and mm == 30:
                                    continue
                                # if marketStatus[sym] == 4:
                                if marketStatus[sym] != 1:  ##selective row when market opened only.
                                    # continue

                                    wr = csv.writer(ref_files2[symbols.index(sym)], lineterminator='\n')
                                    wr.writerow(forTemp[sym])

                                    # np.array(forTemp[sym]).dump(open('array2.npy', 'wb'))

                                else:
                                    wr = csv.writer(ref_files[symbols.index(sym)], lineterminator='\n')
                                    wr.writerow(forTemp[sym])

                                    # sql = "INSERT INTO %s (hour,minute,second,timestamp,bid0,bid1,bid2,bid3,bid4) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                                    #     sym, HH, mm, SS, Timestamp[0], bidOffer[0], bidOffer[1], bidOffer[2],
                                    #     bidOffer[3], bidOffer[4])
                                    #
                                    # try:
                                    #     cursor.execute(sql)
                                    #     # db.commit()
                                    # except Exception as e:
                                    #     print e
                                    #     db.rollback()

                                    # np.array(forTemp[sym]).dump(open('array.npy', 'wb'))

                                    sumOrder[sym] = 0
                                    countOrder[sym] = 0

                            elif 'ava' in jsonDecoded.keys():
                                tim = jsonDecoded["tim"]  ##time
                                HH, mm, SS = getTime(jsonDecoded["tim"])
                                HH = int(HH)
                                mm = int(mm)
                                SS = int(SS)
                                Timestamp = Datetime2Timestamp(datetime(YYYY, MM, DD, HH, mm, SS))  ###
                                Timestamp = checkTimestamp(Timestamp,sym)

                                actVol = jsonDecoded["vol"]  ##vol action
                                prc = jsonDecoded["prc"]  # Last price action(Baht) must / 100
                                lastPrice[sym] = prc

                                # ava = jsonDecoded["ava"]  # Total Trade Value(Baht) must / 100
                                avo = jsonDecoded["avo"]  # Total Trade Volume(Share)
                                tradeVol[sym] = avo

                                bvo = jsonDecoded["bvo"]  # Net Buy Volume(Share)
                                svo = jsonDecoded["svo"]  # Net Sell Volume(Share)
                                ovo = jsonDecoded["ovo"]  # Net ATO/ATC Volume(Share)

                                buyVol[sym] = bvo
                                sellVol[sym] = svo
                                auctVol[sym] = ovo

                                # sid = jsonDecoded["sid"]  ## B = Buy, S = Sell

                                prr = jsonDecoded["prr"]  # Previous Close must / 100
                                hgh = jsonDecoded["hgh"]  # high Price must / 100
                                low = jsonDecoded["low"]  # low Price must / 100
                                avg = jsonDecoded["avg"]  # Average Price must / 100
                                prior[sym] = prr
                                highPrice[sym] = hgh
                                lowPrice[sym] = low
                                avgPrice[sym] = avg

                                sidetransac[sym] = event(jsonDecoded["sid"])

                                sumOrder[sym] += actVol
                                countOrder[sym] += 1

                                if sumOrder[sym] >= 100000:
                                    count100k[sym] = 1
                                else:
                                    count100k[sym] = 0

                                # a = [marketStatus[sym]] + [idSymbol[sym]] + [Timestamp[0]]+ [Timestamp[1]] + [eve] + [Date] + [tim] + [prc] + [actVol] + [avo] + [prr] + [hgh] + [low] + [avg]
                                # wr = csv.writer(ref_files[symbols.index(sym)], lineterminator='\n')
                                # wr.writerow(a)


        db.commit()
# disconnect from server
db.close()


t1 = time.time()
total = t1-t0

print total

