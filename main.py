import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (15,8)
btc = pd.read_csv('BTC-USD.csv',index_col=0)
buy = []
sell = []
profits= []
#Operations tracker
operations = [0]*len(btc)
capital = 100000
def ema(btc, n):
    a = 2/(1+n)
    ema = []
    for j in range(0,len(btc.Close)):
        if j >=26:
            points = 0
            avg = 0
            data = btc.Close[j-n: j:]
            data = data[::-1]
            for i in range(n):
                points += int(data[i])*(1-a)**i
                avg +=(1-a)**i
            ema.append(points / avg)
        else:
            ema.append(0)
    return ema
def signal(btc, n):
    a = 2/(1+n)
    sign = []
    for j in range(0,len(btc.Close)):
        if j >=35:
            points = 0
            avg = 0
            data = btc.macd[j-n: j:]
            data = data[::-1]
            for i in range(n):
                points += int(data[i])*(1-a)**i
                avg +=(1-a)**i
            sign.append(points / avg)
        else:
            sign.append(0)
    return sign

def macd(btc):
    btc['ema12'] = ema(btc,12)
    btc['ema26'] = ema(btc,26)
    btc['macd'] = btc.ema12 - btc.ema26
    btc['signal'] = signal(btc,9)

def buy_sell(btc):
    for i in range(36, len(btc)):
        if btc.macd.iloc[i] > btc.signal.iloc[i] and btc.macd.iloc[i - 1] < btc.signal.iloc[i - 1]:
            buy.append(i)
            # Adding option BUY(=1) to our tracker
            operations[i+1] = 1
        elif btc.macd.iloc[i] < btc.signal.iloc[i] and btc.macd.iloc[i - 1] > btc.signal.iloc[i - 1]:
            sell.append(i)
            # Adding option SELL(=2) to our tracker
            operations[i+1] = 2
    #In case when we have selling as a first option or buying as a last - we need to delete these options
    if sell[0] < buy[0]:
        operations[sell[0]+1] = 0
        sell.pop(0)
    if buy[-1] > sell[-1]:
        operations[buy[-1] + 1] = 0
        buy.pop(-1)

def badProfit(capital = None):
    end_capital = capital
    for i in range(len(realBuyPrices)):
        profits.append(((realSellPrices[i]-realBuyPrices[i])/realBuyPrices[i]))
        #Calculating gain/loss percent after current transaction
        temp = end_capital * abs(profits[i])
        #Gain
        if profits[i]>0:
            end_capital = end_capital+temp
        #Loss
        elif profits[i]<0:
            end_capital = end_capital -temp
    return end_capital
def goodProfit(capital = None):
    start_stocks_number = 1000
    end_capital = capital
    number = 50
    print('Start wallet:{}$'.format(capital+start_stocks_number*realBuyPrices[0]))
    for i in range(35,len(operations)):
        # if we have BUYING(=1) option on tracker, we need to buy stocks with a price of i-th day
        if operations[i]==1:
            start_stocks_number+=number
            end_capital-=number*realBuyPrices[realbuy.index(i)]
        # if we have SELLING(=2) option on tracker, we need to sell stocks with a price of i-th day
        elif operations[i]==2:
            start_stocks_number-=number
            end_capital+=number*realSellPrices[realsell.index(i)]
    print('End wallet:{}$'.format(end_capital + start_stocks_number * realBuyPrices[-1]))
    print('Profit: {}%'.format(percent(capital+start_stocks_number*realBuyPrices[0], end_capital + start_stocks_number * realBuyPrices[-1])))
def macd_graph():
    plt.title('MACD-Signal graph')
    plt.xlabel('Date')
    plt.ylabel('MACD/Signal values')

    plt.plot(btc.signal, label = 'Signal',color = 'orange')
    plt.plot(btc.macd, label = 'MACD',color = 'dodgerblue')
    plt.xticks(range(0, len(btc), 100))
    plt.legend()
    plt.grid(True)
    plt.show()

def stocks_graph():
    plt.title('Stocks graph with buy-sell indicators')
    plt.xlabel('Date')
    plt.ylabel('Stock price')

    plt.plot(btc.Close,color = 'black')
    plt.scatter(btc.iloc[buy].index, btc.iloc[buy].Close, marker=6, color ='green')
    plt.scatter(btc.iloc[sell].index, btc.iloc[sell].Close, marker=7, color ='red')

    plt.xticks(range(0, len(btc), 100))
    plt.grid(True)
    plt.show()
def percent(capital = None, final_capital = None):
    stonks = 100*(final_capital-capital)/capital
    return int(stonks)

#Macd and stocks graph with Buy-Sell indicators
macd(btc)
macd_graph()
buy_sell(btc)
stocks_graph()

#There is only one possible way to buy a stock - next day after getting Close prise, buy it with Open price
realbuy = [i + 1 for i in buy]
realsell = [i + 1 for i in sell]
realBuyPrices = btc.Open.iloc[realbuy]
realSellPrices = btc.Open.iloc[realsell]

#In case when we have selling as a first option or buying as a last - we need to delete these options
if realSellPrices.index[0] < realBuyPrices.index[0]:
    realSellPrices = realSellPrices.drop(realSellPrices.index[0])
if realBuyPrices.index[-1] > realSellPrices.index[-1]:
    realBuyPrices = realBuyPrices.drop(realBuyPrices.index[-1])
print('\n---GOOD-PROFIT---')
print('\nLet\'s take a look at final capital and profit percentage after using MACD with a starting capital {}$'.format(capital))
print('For that we analizing BTC stocks from 2019 till 2020')
print('Here is proper way to calculate the profit')
print('In this case we have 1000 stocks at start, and with every transaction we will buy and sell 50 stocks')
goodProfit(capital)
print('\n---BAD-PROFIT---')
final_capital = badProfit(capital)
print('Here is not the best way to calculate the profit')
print('We don\'t have start amount of stocks, we just have our start capital and with every trade we will invest all our money')
print('Final capital: {}$'.format(final_capital))
print('Profit: {}%'.format(percent(capital,final_capital)))
