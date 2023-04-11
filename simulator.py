import pandas
import functions

CSV_ROWS = 1000

def simulator():
    data = pandas.read_csv("lor_de_d.csv", nrows=CSV_ROWS)
    money = 1000
    actions = 0
    print("Starting money: ", money)
    functions.sharePricePlot(data)
    functions.calcMACDInd(data)
    functions.calcSignal(data)
    functions.macdSignalPlot(data)
    money, actions = functions.findCrossings(data, money, actions)

    print("Money after all transactions: ", money)
    print("Number of actions after all transactions: ", actions)

    price = data.loc[CSV_ROWS-1, 'Open'] * actions
    actions = 0
    money += price
    print("If we sell all actions in the last day we have ", money, " money and", actions, " actions")




