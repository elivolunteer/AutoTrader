import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import style
import mplfinance as fplt
import matplotlib.dates as mdates
import pandas_datareader.data as web

style.use("ggplot")

start = dt.datetime(2008,1,1)
end = dt.datetime(2016,1,1)

df = web.DataReader("AAPL", "yahoo", start, end)

#resample
df_ohlc = df["Adj Close"].resample("10D").ohlc()
df_volume = df["Volume"].resample("10D").sum()

fplt.plot(df_ohlc, type="candle", style="charles", title="Apple 2008-2016", ylabel="Price")

print(df_ohlc.head())
