import yfinance as yf
import pandas as pd
import json

def reformatTickers(tickers):
    return set([ticker.replace(".", "-") for ticker in tickers])

def getStockData(ticker):
    data = yf.download(ticker, progress=False)
    data.reset_index(inplace=True)
    data = data[["Date", "Open", "High", "Low", "Close", "Volume"]].values.tolist()
    for i, _ in enumerate(data):
        data[i][0] = str(data[i][0])
    return data

def saveData(data, path):
    with open(path, "w+") as file:
        file.write(json.dumps(data))

NASDAQTickers = sorted(pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")[4]["Symbol"].tolist())
SP500Tickers = sorted(pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]["Symbol"].tolist())
DowJonesTickers = sorted(pd.read_html("https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average")[2]["Symbol"].tolist())

allTickers = reformatTickers([*NASDAQTickers, *SP500Tickers, *DowJonesTickers])
allTickersl = len(allTickers)

i = 0
for ticker in allTickers:
    data = getStockData(ticker)

    if not data:
        print(f"Skipping {data}: No data found.")
        continue

    saveData(data, f"./bin/stocks/{ticker}.json")

    i += 1

    print("\r", i / allTickersl * 100, "%", " " * 10, end="", sep="")
