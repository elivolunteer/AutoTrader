import alpaca_config
import alpaca_trade_api as tradeapi
import datetime, time, sys
import pickle
import UpdateAndRetrain
from trade import Trade

def main():
    #Check command line arguments
    if len(argv) < 3 or len(argv) > 3:
        print("Usage: Alpaca_Connection.py <Industry> (IT, HC, Energy) <Strategy> (SVM) <Mode>")

    # Connect to Alpaca
    BASE_URL = "https://paper-api.alpaca.markets"
    alpaca = tradeapi.REST(alpaca_config.API_KEY, alpaca_config.SECRET_KEY, BASE_URL)
    account = alpaca.get_account()

    # This should run "forever" on the pi, but only once a day
    while(True):
        # Retrain if it's midnight
        currentDT = datetime.datetime.now()
        if (currentDT.hour == 0):
            UpdateAndRetrain.main(['UpdateAndRetrain.py', argv[1], argv[2]])
        # Check if the market is open now.
        clock = alpaca.get_clock()
        if clock.is_open == True:
            print(f"The market is open at {clock.timestamp}")
            # At noon, execute stragety
            tickers = pickle.load(f"tickers/{argv[1]}_tickers.pickle")
            for ticker in tickers
                # TODO: check money,
                #       execute,
                #       add to csv
        else:
            print(f"The market is closed at {clock.timestamp}")

        time.sleep(3600)


if __name__ == "__main__":
    main()
