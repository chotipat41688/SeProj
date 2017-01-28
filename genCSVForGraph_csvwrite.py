symbols = ["SPPT"]

# items= ["2016-12-09_FANCY_30"]
# items= ["2016-12-09_FANCY_30","2016-10-13","2016-10-14","2016-11-11","2016-11-14","2016-11-15","2016-11-30","2016-12-14_30","2016-12-15_30"]



# items= ["TEST_2017-01-18"]
items= ["Sample"]




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

    if price[0] == 0:
        price[0] = priATO[symbol]

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
priATO = dict()


for symbol in symbols:
    tempBid[symbol] = [None, None, None, None, None, None, None, None, None, None]
    tempOffer[symbol] = [None, None, None, None, None, None, None, None, None, None]
    priATO[symbol] = 0

for symbol in symbols:
    tempBidVol[symbol] = []
    tempOffVol[symbol] = []


ref_files = [open("TESTWRITE\\List\\" + Symbol + ".csv", "a") for Symbol in symbols]

for Date in items:

    # YYYY,MM,DD = getDate(Date)
    #
    # YYYY = [YYYY]
    # MM = [MM]
    # DD = [DD]

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

                                # hh, mm, ss = getTime(jsonDecoded["tim"])    #time
                                tim = jsonDecoded["tim"]    #time


                                # priATO[sym] = pri

                                vol = jsonDecoded["vol"]  # volume
                                op1 = jsonDecoded["op1"]  # open1
                                op2 = jsonDecoded["op2"]  # open2



                                # a = [None] + YYYY + MM + DD + [hh] + [mm] + [ss] + [pri] + [vol] + [op1] + [op2]
                                a = [None] + [Date] + [tim] + [pri] + [vol] + [op1] + [op2]

                                # isf = jsonDecoded["isf"]    #isFinal? True or False
                                # if pri != 0 and vol != 0:
                                #     a = (str(id) + ',5,'  + str(hh) + ',' + str(mm) + ',' + str(ss) + ',' + str(pri) + ',' + str(vol) + ',' + str(op1) + ',' + str(op2)) + ',' + str(totalVol)
                                #     output.writelines(a + '\n')
                                wr = csv.writer(ref_files[symbols.index(sym)], lineterminator='\n')
                                wr.writerow(a)


                            if 'time' in jsonDecoded.keys():
                                pri = jsonDecoded["pri"]
                                if check(pri) is 0: continue

                                eve = event(jsonDecoded["sid"])
                                # hh, mm, ss = getTime(jsonDecoded["time"])
                                tim = jsonDecoded["time"]
                                id = jsonDecoded["id"]  ##identify number of stock
                                vol = jsonDecoded["vol"]

                                # a = [id] + YYYY + MM + DD + [hh] + [mm] + [ss] + toTemp(pri, vol, eve, sym)
                                a = [id] + [Date] + [tim] + toTemp(pri, vol, eve, sym)

                                wr = csv.writer(ref_files[symbols.index(sym)], lineterminator='\n')
                                wr.writerow(a)

                            # if 'ava' in jsonDecoded.keys():
                            #     # tim = jsonDecoded["tim"]  ##time
                            #     hh, mm, ss = getTime(jsonDecoded["tim"])
                            #     actVol = jsonDecoded["vol"]  ##vol action
                            #     prc = jsonDecoded["prc"]  # Last price action(Baht) must / 100
                            #     # ava = jsonDecoded["ava"]  # Total Trade Value(Baht) must / 100
                            #     avo = jsonDecoded["avo"]  # Total Trade Volume(Share)
                            #
                            #     # bvo = jsonDecoded["bvo"]  # Net Buy Volume(Share)
                            #     # svo = jsonDecoded["svo"]  # Net Sell Volume(Share)
                            #     # ovo = jsonDecoded["ovo"]  # Net ATO/ATC Volume(Share)
                            #     # sid = jsonDecoded["sid"]  ## B = Buy, S = Sell
                            #     prr = jsonDecoded["prr"]  # Previous Close must / 100
                            #     hgh = jsonDecoded["hgh"]  # high Price must / 100
                            #     low = jsonDecoded["low"]  # low Price must / 100
                            #     avg = jsonDecoded["avg"]  # Average Price must / 100
                            #     eve = event(jsonDecoded["sid"]) + 2

                                # a =  [None] + YYYY + MM + DD + [hh] + [mm] + [ss] + [eve] + [prc] + [actVol] + [avo] + [prr] + [hgh] + [low] + [avg]
                                #
                                # wr = csv.writer(ref_files[symbols.index(sym)], lineterminator='\n')
                                # wr.writerow(a)




t1 = time.time()


total = t1-t0

print total

