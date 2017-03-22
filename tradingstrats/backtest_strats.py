#
# Sample script for backtesting
#

#To show the chart inline in jupyter notebook...
%matplotlib inline 

import matplotlib.pyplot as plt
import numpy as np
import datetime
import pandas as pd
import datetime

#trading strategy library
import quantlib.trading_strat as strat
from bokeh import mpl


#import quantlib as pdt

##using numpy 
#n1=np.arange(100).reshape(50,2)
#x = np.array([datetime.datetime(2017,1, 18 ,i,0) for i in range(24)])
#y = np.random.randint(100, size=x.shape)

##use pandas DataFrame
#ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
#ts = ts.cumsum()

##plot numpy data
#plt.plot(x,y)
#plt.show()

##plot dataframe data
#ts = ts.cumsum()
#ts.plot()

#trading strat example
bars = strat.history_data('AAPL', datetime.datetime(2008, 1, 1), datetime.datetime(2010,1,1))
#print bars.head
mac = strat.MovingAverageCrossStrategy('AAPL', bars, short_window=40, long_window=100)
# Create a Moving Average Cross Strategy instance 
# with short and long moving average windows
signals = mac.generate_signals()

# Create a portfolio of AMZN, with $100,000 initial capital
portfolio = strat.MarketOnClosePortfolio('AMZN', bars, signals, initial_capital=100000.0)
returns = portfolio.backtest_portfolio()

# Plot two charts to assess trades and equity curve
fig = plt.figure()
fig.patch.set_facecolor('white')     # Set the outer colour to white
ax1 = fig.add_subplot(211,  ylabel='Price in $')

# Plot the AMZN closing price overlaid with the moving averages
bars['Adj Close'].plot(ax=ax1, color='r', lw=2.)
signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)


# Plot the "buy" trades against AMZN
ax1.plot(signals.ix[signals.positions == 1.0].index,
         signals.short_mavg[signals.positions == 1.0],
         '^', markersize=10, color='m')

# Plot the "sell" trades against AMZN
ax1.plot(signals.ix[signals.positions == -1.0].index,
         signals.short_mavg[signals.positions == -1.0],
         'v', markersize=10, color='k')

# Plot the equity curve in dollars
ax2 = fig.add_subplot(212, ylabel='Portfolio value in $')
returns['total'].plot(ax=ax2, lw=2.)

# Plot the "buy" and "sell" trades against the equity curve
ax2.plot(returns.ix[signals.positions == 1.0].index,
         returns.total[signals.positions == 1.0],
         '^', markersize=10, color='m')
ax2.plot(returns.ix[signals.positions == -1.0].index,
         returns.total[signals.positions == -1.0],
         'v', markersize=10, color='k')
fig.set_size_inches(16.5, 8.5)
# Plot the figure

fig.show()
mpl.to_bokeh(fig)



