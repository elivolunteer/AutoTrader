import alpaca_config
import alpaca_trade_api as tradeapi
import datetime, time, sys
import pickle
import UpdateAndRetrain
import SP500
from trade import Trade

def main():
    #Check command line arguments
    if len(argv) < 3 or len(argv) > 3:
        print("Usage: Alpaca_Connection.py <Industry> (IT, HC, Energy) <Strategy> (svm) <Mode>")

    # Connect to Alpaca
    BASE_URL = "https://paper-api.alpaca.markets"
    alpaca = tradeapi.REST(alpaca_config.API_KEY, alpaca_config.SECRET_KEY, BASE_URL)
    account = alpaca.get_account()

    # This should run "forever" on the pi, but only once a day
    while(True):
        # reload data if it's midnight
        currentDT = datetime.datetime.now()
        if (currentDT.hour == 0):
            SP500.get_data_from_yahoo(reload_sp500=False)
            UpdateAndRetrain.main(['UpdateAndRetrain.py', argv[1], argv[2]])
            #retrain if it's monday
            if (currentDT.today().weekday() == 0):
                UpdateAndRetrain.main(['UpdateAndRetrain.py', argv[1], argv[2]])
        # Check if the market is open now.
        clock = alpaca.get_clock()
        if clock.is_open == True:
            print(f"The market is open at {clock.timestamp}")
            # At noon, execute stragety
            tickers = pickle.load(f"tickers/{argv[1]}_tickers.pickle")
            clf = pickle.load(f"strategies/{argv[1]}+{argv[2]}_clf")

            for ticker in tickers:
                # get the last "waveform"
                waveform = curr_waveform(ticker)
                bsh = clf.predict(waveform)
                if (bsh == 1): # BUY CASE
                    #only buy if it's less than 0.1% of our current buying power
                    bp = account.buying_power
                    if (waveform[-1] < 0.1*bp):
                        alpaca.submit_order(ticker, 1, "buy", "market", "gtc")
                if (bsh == -1): # SELL CASE
                    #only sell if we actually have it
                    if (alpaca.get_position(ticker).qty > 0):
                        alpaca.submit_order(ticker, 1, "sell", "market", "gtc")
                # TODO: check money,
                #       execute,
                #       add to csv
        else:
            print(f"The market is closed at {clock.timestamp}")

        time.sleep(3600)

def curr_waveform(ticker):
    hm_days = 30 #amount of days in the "waveform"
    with open("stock_dfs/{}.pickle".format(ticker), "rb") as f:
        df = pickle.load(f)

    waveform = np.zeros(hm_days)
    for i in range(hm_days, 0, -1):
        #append the data as waveforms
        tmp[i-1] = df.iloc[len(df)-1-day-i]["Adj Close"]

    return waveform

if __name__ == "__main__":
    main()
