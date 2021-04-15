import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import style
import pandas_datareader.data as web

style.use("ggplot")

start = dt.datetime(2008,1,1)
end = dt.datetime(2016,1,1)

df = web.DataReader("AAPL", "yahoo", start, end)

df["100ma"] = df["Adj Close"].rolling(window=100, min_periods=0).mean()
#doesn't exist for first 100 days, can drop the rows without using df.dropna(inplace=True)
print(df.head())

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=True)

ax1.plot(df.index, df["Adj Close"])
ax1.plot(df.index, df["100ma"])
ax2.bar(df.index, df["Volume"])
plt.show()
