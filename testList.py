# eiei = [36,42,53]
# print(type(eiei),eiei,eiei[0])
# print(len(eiei))

# import pandas as pd
# adult = pd.read_json("TESTDATA\\ATOATCData.txt")
# adult.head()

# import pandas as pd
# from pandas import DataFrame
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
#
# df = pd.read_csv('TESTDATA\\ATOATCData2016-11-14.csv', parse_dates=True)
# print(df.head())
#
# df['25MA'] = pd.rolling_mean(df['Price'], 25)
#
# threedee = plt.figure().gca(projection='3d')
# threedee.scatter(df.index, df['25MA'], df['Price'])
# threedee.set_xlabel('Volume')
# threedee.set_ylabel('Price')
# threedee.set_zlabel('Open2')
# plt.show()

# from _datetime import datetime
# def validate(date_text):
#     try:
#         datetime.datetime.strptime(date_text, '%Y-%m-%d')
#     except ValueError:
#         raise ValueError("Incorrect data format, should be YYYY-MM-DD")
#
# d = datetime.date('2012-9-1 19:30:00')
# print (type(d) is datetime.date)


def getFreefloat():
    allShare = 250000000  # ACAP
    freeFloat = 67.03

    return (allShare * freeFloat)/100



def check(list):
    if list[3] is not 0 and list[4] is 0: return 0
    else: return 1

def getSumOffer(list):
    # sum = float(list[0]+list[1]+list[2]+list[3]+list[4])
    Sum = float(list[0] + list[1] + list[2] + list[3] + list[4])
    # list0=format(list[0]/sum,'.2f')
    Avg = Sum/5
    list0 = int(list[0] / Avg * 100)
    list1 = int(list[1] / Avg * 100)
    list2 = int(list[2] / Avg * 100)
    list3 = int(list[3] / Avg * 100)
    list4 = int(list[4] / Avg * 100)
    return Sum,list0,list1,list2,list3,list4


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


id = 0
lastPrice = 0
prior = 0
totalVol = 0
op1=0
op2=0


for Date in items:

    YYYY,MM,DD = getDate(Date)

    with open("INPUT\\" +Date+".dat") as f, open("TESTWRITE\\FANCY_testnewVol" + items[0] + "to" + items[-1] + ".csv", "a") as output:         ## One file Many Day
    # with open(Date + ".dat") as f, open("TESTWRITE\\cutword_IFEC_event" + Date + ".txt", "a") as output:      ## One file One Day
        content = f.readlines()
        for line in content:
            if ('data' in line):
                jsonData = line.replace("data: ", "")
                jsonDecoded = json.loads(jsonData)
                if 'sym' in jsonDecoded.keys():
                    if jsonDecoded["sym"] == "FANCY":
                        if 'ava' in jsonDecoded.keys():
                            # tim = jsonDecoded["tim"]  ##time
                            hh,mm,ss = getTime(jsonDecoded["tim"])
                            actVol = jsonDecoded["vol"]  ##vol action
                            prc = jsonDecoded["prc"]  # Last price action(Baht) must / 100
                            # ava = jsonDecoded["ava"]  # Total Trade Value(Baht) must / 100
                            avo = jsonDecoded["avo"]  # Total Trade Volume(Share)
                            totalVol = avo  ###---###
                            # bvo = jsonDecoded["bvo"]  # Net Buy Volume(Share)
                            # svo = jsonDecoded["svo"]  # Net Sell Volume(Share)
                            # ovo = jsonDecoded["ovo"]  # Net ATO/ATC Volume(Share)
                            # sid = jsonDecoded["sid"]  ## B = Buy, S = Sell
                            prr = jsonDecoded["prr"]  # Previous Close must / 100
                            hgh = jsonDecoded["hgh"]  # high Price must / 100
                            low = jsonDecoded["low"]  # low Price must / 100
                            avg = jsonDecoded["avg"]  # Average Price must / 100
                            eve = event(jsonDecoded["sid"])+2

                            a = str(id) + ','+ str(eve) + ',' + str(hh) + ',' + str(mm) + ',' + str(ss) + ',' + str(prc) + ',' + str(actVol)  + ',' + \
                                str(avo)  + ',' + str(prr) + ',' + str(hgh) + ',' + str(low) + ',' + str(avg) + ',' + str(totalVol)
                            output.writelines(a + '\n')
    #                         # print(tim,",vol:",actVol,",price",prc,ava,avo,bvo,svo,ovo,sid,prr,hgh,low,avg)


                        if 'time' in jsonDecoded.keys():
                            pri = jsonDecoded["pri"]


                            if check(pri) is 0: continue
                                                                    #get percent freefloat compare between sum vol offer, all share
                            eve = event(jsonDecoded["sid"])
                            hh, mm, ss = getTime(jsonDecoded["time"])
                            id = jsonDecoded["id"]  ##identify number of stock
                            vol = jsonDecoded["vol"]
                            # sumVO,RO0,RO1,RO2,RO3,RO4 = getSumOffer(vol)  #Fix bug ZeroDiv




                            # if jsonDecoded["sid"] is 'S':  # sid: B is Bid side, S is Offer side
                            #     sid = 1  # Fill Offer
                            #     offerPrice = jsonDecoded["pri"]  # There are List 5 Price must / 100
                            #     offerVol = jsonDecoded["vol"]  # There are List 5 Price
                            # else:
                            #     sid = 0  # Fill Bid
                            #     pri = jsonDecoded["pri"]  # There are List 5 Price must / 100
                            #     bidPrice = pri[::-1]  # pri.reverse()
                            #     vol = jsonDecoded["vol"]  # There are List 5 Price
                            #     bidVol = pri[::-1]  # pri.reverse()
                            Temp = str(pri[0])+ ',' + str(pri[1])+ ',' + str(pri[2])+ ',' + str(pri[3])+ ',' + str(pri[4]) + ',' + str(vol[0])+ ',' + str(vol[1])+ ',' + str(vol[2])+ ',' + str(vol[3])+ ',' + str(vol[4])


                            # a = str(id)+ ',' + str(eve) + ',' + str(hh) + ',' + str(mm) + ',' + str(ss)  + ',' + toTemp(Temp,eve)+ ',' + str(sumVO)+ ',' + str(RO0)+ ',' + str(RO1)+ ',' + str(RO2)+ ',' + str(RO3)+ ',' + str(RO4)+',' + str(totalVol)

                            a = str(id) + ',' + str(eve) + ',' + str(hh) + ',' + str(mm) + ',' + str(ss) + ',' + toTemp(Temp, eve,vol)  + ',' + str(totalVol)    #Fix bug ZeroDiv

                            output.writelines(a + '\n')

                        if 'isf' in jsonDecoded.keys():  #### get wanted Data ("isf" is about Proj.Price and Proj.Vol @ ATO/ATC)
                            #                             #### 'isf': 'T' is Confirmed Proj. and use data before this state  (use latest 'isf': 'F')
                            #                             #### 'isf': 'T' tag is use to find time that ATO/ATC is take action.
                            # pri = jsonDecoded["pri"]  # price
                            # sym = jsonDecoded["sym"]  # symbol
                            # hh, mm, ss = getTime(jsonDecoded["tim"])    #time
                            # vol = jsonDecoded["vol"]  # volume
                            op1 = jsonDecoded["op1"]  # open1
                            op2 = jsonDecoded["op2"]  # open2
                            # isf = jsonDecoded["isf"]    #isFinal? True or False
                            # if pri != 0 and vol != 0:
                            #     a = (str(id) + ',5,'  + str(hh) + ',' + str(mm) + ',' + str(ss) + ',' + str(pri) + ',' + str(vol) + ',' + str(op1) + ',' + str(op2)) + ',' + str(totalVol)
                            #     output.writelines(a + '\n')



    with open("STOCK\\" + str(id)  + ".csv", "a") as update:
        update.writelines(str(YYYY)+","+str(MM)+","+str(DD)+","+str(totalVol)+","+str(prr)+","+str(op1)+","+str(op2)+","+str(prc) +","+str(hgh)+","+str(low)+","+str(avg)+ '\n')



