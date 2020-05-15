# -*- coding: utf-8 -*-
"""
Created on Fri May 15 07:52:38 2020

@author: Lakshmikanth
@Source: https://plotly.com/python/
"""
import plotly.graph_objects as go
import plotly.express as px
import dateutil.relativedelta
import matplotlib.pyplot as plt

from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
from nsepy import get_history
from datetime import datetime , date

StockSymbol = 'RELIANCE'

# data from annual reports
# Note: This is just a sample data
sales = 27,501.00 
expenses = -18,531.00 
operating_profit = 8,970.00 
other_Income = 1,211.00 
depreciation = -854.00 
interest = -2.00 
profit_before_tax = 9,325.00 
tax = -2,490.00 
net_profit = 6,835.00 

to_date = datetime.now()

to_date = datetime.strftime(to_date, '%Y,%m,%d %H,%M,%S')
to_date = datetime.strptime(to_date, '%Y,%m,%d %H,%M,%S')
from_date = to_date-dateutil.relativedelta.relativedelta(months = 12)

data = get_history(symbol=StockSymbol, 
                   start =from_date , 
                   end = to_date)
data.reset_index(level=0, inplace=True)

# Plotting the time s
fig = px.line(data, x='Date', y='Close')
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
#plot(fig)

#Plotting the candlestick charts
fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                increasing_line_color= 'green', decreasing_line_color= 'red'
                )])
fig.update_layout(xaxis_rangeslider_visible=True)
fig.update_layout(
    title='Historical data',
    yaxis_title='Price',
    xaxis_title='Date'
)
#plot(fig)

data['Daily returns'] = data['Close'][:-1] / data['Close'][1:].values - 1
#print(data['Daily returns'].head())
data['Daily returns'].dropna()
#plt.hist(data['Daily returns'], bins = 5)

data.boxplot(column = 'Close');
plt.title('')

fig = go.Figure(go.Waterfall(
    name = "20", orientation = "v",
    measure = ["relative", "relative", "total", "relative", "relative", "relative" 
               ,"total","relative" ,"total"],
    x = ["Sales", "expenses", "operating_profit", "other_Income", "depreciation", "interest"
         , "profit_before_tax" , "tax", "net_profit"],
    textposition = "inside",
    text = [str(sales) , str(expenses) , str(operating_profit) , str(other_Income), str(depreciation), str(interest)
           , str(profit_before_tax),  str(tax) , str(net_profit)] ,
    y = [27501, -18531 , 0 , 1211, -854, -2 ,
         0 ,  -2490, 0] ,
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
))

fig.update_layout(
        title = "Profit and loss statement 2020",
        waterfallgap = 0.3,
        showlegend = True
)

#plot(fig)

