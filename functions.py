from matplotlib import pyplot 
import math
import numpy

CSV_ROWS = 1000

def sharePricePlot(data):
    x = numpy.arange(len(data))
    every_nth = 199
    x_ticks = x[::every_nth]
    pyplot.plot(data.loc[0:CSV_ROWS,'Date'], data.loc[0:CSV_ROWS, 'Open'])
    pyplot.ylabel('Value')
    pyplot.xlabel('Date')
    pyplot.title('Daily stock exchange price of L\'OREAL from  25-04-2019 to 28-03-2023')
    pyplot.margins(0.0, 0.0)
    pyplot.xticks(x_ticks, data.loc[1:CSV_ROWS:every_nth, 'Date'])
    pyplot.grid()
    pyplot.savefig("sharePricePlot.png")
    pyplot.show()
    pyplot.close()

def macdSignalPlot(data):
    x = numpy.arange(len(data))
    every_nth = 199
    x_ticks = x[::every_nth]
    pyplot.plot(data.loc[0:CSV_ROWS, 'Date'], data.loc[0:CSV_ROWS, 'MACD'], label='MACD', color='blue', linewidth=0.5)
    pyplot.plot(data.loc[0:CSV_ROWS, 'Date'], data.loc[0:CSV_ROWS, 'Signal'], label='SIGNAL', color='red', linewidth=0.5)
    pyplot.title('MACD and SIGNAL indicator')
    pyplot.margins(0.0, 0.0)
    pyplot.xlabel('Date')
    pyplot.ylabel('Rate')
    pyplot.legend(loc="upper left")
    pyplot.xticks(x_ticks, data.loc[1:CSV_ROWS:every_nth, 'Date'])
    pyplot.grid()
    pyplot.savefig("macdSignalPlot.png")
    pyplot.show()
    pyplot.close()


def calculateEMA(data, n, i, column):
    num = float(0.0)
    den = float(0.0)
    alpha = 2/(n+1)
    if (i - n) < 0:
        return 0
    for j in range(i, i - n, -1):
        p = float(data.loc[j, column])
        num += float(p * (1-alpha)**j)
        den += float((1-alpha)**j)
    ema = num/den
    return ema


def calcMACDInd(data):
    data['MACD'] = 0
    for i in range(CSV_ROWS):
        if (i - 26) > 0:
            ema12 = calculateEMA(data, 12, i, 'Open')
            ema26 = calculateEMA(data, 26, i, 'Open')
            data.loc[i:i, 'MACD'] = ema12 - ema26

def calcSignal(data):
    data['Signal'] = 0
    for i in range(CSV_ROWS):
        data.loc[i:i, 'Signal'] = calculateEMA(data, 9, i, 'MACD')



def buy(money, actions, data, i, nbOfTransaction):
    print("Transaction number: ", nbOfTransaction)
    nbOfTransaction += 1
    print("Money before buying actions: ", money)
    print("Amount of actions before buying: ", actions)
    price = data.loc[i, 'Open']
    amount = math.floor(money / price)
    if money - amount*price >= 0:
        actions += amount
        money -= float(amount*price)
        print("Money after buying actions: ", money)
        print("Amount of actions after buying: ", actions)
        print("\n")
    else:
        print("Not enough money to buy actions")
    return money, actions, nbOfTransaction

def sell(money, actions, data, i, nbOfTransaction):
    print("Transaction number: ", nbOfTransaction)
    nbOfTransaction += 1
    print("Money before selling actions: ", money)
    print("Amount of actions before selling: ", actions)
    price = data.loc[i, 'Open']
    amount = actions*price
    money += amount
    actions = 0
    print("Money after selling actions: ", money)
    print("Amount of actions after selling: ", actions)
    print("\n")
    return money, actions, nbOfTransaction



def findCrossings(data, money, actions):
    nbOfTransaction = 1
    macdUp = True
    macdUpTemp =True
    m = data.loc[27, 'MACD']
    s = data.loc[27, 'Signal']
    if m < s:
        macdUp = False
        macdUpTemp = False
    for i in range(27, CSV_ROWS):
        m = data.loc[i, 'MACD']
        s = data.loc[i, 'Signal']
        if m < s:
            macdUp = False
        else:
            macdUp = True
        if macdUp != macdUpTemp:
            macdUpTemp = macdUp
            if macdUp:
                money, actions, nbOfTransaction = buy(money, actions, data, i, nbOfTransaction)
            else:
                money, actions, nbOfTransaction = sell(money, actions, data, i, nbOfTransaction)

    return money, actions

