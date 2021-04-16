import datetime as dt
import numpy as np
import pandas as pd
import pickle

def create_labels(df, tickers):
    hm_days = 30 #amount of days in the "waveform"
    datelist = pd.date_range(start="1/1/2015", end="10/22/2020", freq="D") #needs to have buffer of at least hm_days
    print(len(df))

    waveforms = np.zeros(hm_days)
    labels = []

    for ticker in tickers:
        print("Generating training data from {}".format(ticker))

        #each day, go back through the previous hm_days and create a waveform.
        #calculate the average of last hm days and if the pct diff between day and average is
        # <%5 label buy, >%-5 label sell, otherwise label hold
        for day in range(len(datelist)):
            tmp = np.zeros(hm_days)
            avg = 0
            for i in range(hm_days, 0, -1):
                avg += df.iloc[len(df)-1-day-i][ticker]
                #append the data as waveforms
                tmp[i-1] = df.iloc[len(df)-1-day-i][ticker]
            waveforms = np.vstack((waveforms, tmp))

            #calculate average, then check current, depending on %diff, buy, sell, hold
            avg = avg/hm_days
            pct_diff = (df.iloc[len(df)-1-day][ticker]-avg)/avg

            #decide to buy sell or hold
            req = 0.05
            if pct_diff > req:
                labels.append(1)
            elif pct_diff < -req:
                labels.append(-1)
            else:
                labels.append(0)
    print(waveforms)
    print(labels)

    return waveforms, labels

def genIT_bsh():
    main_df = pd.DataFrame()
    with open("tickers/IT_tickers.pickle", "rb") as f:
        IT_tickers = pickle.load(f)

    for ticker in IT_tickers:
        with open("stock_dfs/{}.pickle".format(ticker), "rb") as f:
            df = pickle.load(f)

        #just keep adj close
        df.rename(columns = {"Adj Close" : ticker}, inplace=True)
        df.drop(["Open", "High", "Low", "Close", "Volume"], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how="outer")

    #main_df = main_df.transpose()
    main_df.fillna(0, inplace=True)
    print(main_df)

    IT_waveforms, IT_labels = create_labels(main_df, IT_tickers)

    #store for analysis
    with open("serialized_data/IT_waveforms.pickle", "wb") as f:
        pickle.dump(IT_waveforms, f)
    with open("serialized_data/IT_labels.pickle", "wb") as f:
        pickle.dump(IT_labels, f)

def genHC_bsh():
    main_df = pd.DataFrame()
    with open("tickers/HC_tickers.pickle", "rb") as f:
        HC_tickers = pickle.load(f)

    for ticker in HC_tickers:
        with open("stock_dfs/{}.pickle".format(ticker), "rb") as f:
            df = pickle.load(f)

        #just keep adj close
        df.rename(columns = {"Adj Close" : ticker}, inplace=True)
        df.drop(["Open", "High", "Low", "Close", "Volume"], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how="outer")

    #main_df = main_df.transpose()
    main_df.fillna(0, inplace=True)
    print(main_df)

    HC_waveforms, HC_labels = create_labels(main_df, HC_tickers)

    #store for analysis
    with open("serialized_data/HC_waveforms.pickle", "wb") as f:
        pickle.dump(HC_waveforms, f)
    with open("serialized_data/HC_labels.pickle", "wb") as f:
        pickle.dump(HC_labels, f)

def genEnergy_bsh():
    main_df = pd.DataFrame()
    with open("tickers/Energy_tickers.pickle", "rb") as f:
        Energy_tickers = pickle.load(f)

    for ticker in Energy_tickers:
        with open("stock_dfs/{}.pickle".format(ticker), "rb") as f:
            df = pickle.load(f)

        #just keep adj close
        df.rename(columns = {"Adj Close" : ticker}, inplace=True)
        df.drop(["Open", "High", "Low", "Close", "Volume"], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how="outer")

    #main_df = main_df.transpose()
    main_df.fillna(0, inplace=True)
    print(main_df)

    Energy_waveforms, Energy_labels = create_labels(main_df, Energy_tickers)

    #store for analysis
    with open("serialized_data/Energy_waveforms.pickle", "wb") as f:
        pickle.dump(Energy_waveforms, f)
    with open("serialized_data/Energy_labels.pickle", "wb") as f:
        pickle.dump(Energy_labels, f)
