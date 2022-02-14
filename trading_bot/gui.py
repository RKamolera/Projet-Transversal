import plotly.graph_objects as go

import json
from datetime import datetime

import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig = px.line(df, x='Date', y='AAPL.High', title='Time Series with Range Slider and Selectors')

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

open_prices = []
high_prices = []
dates = []
low_prices = []
close_prices = []

with open("candle_sample.txt", "r") as fp:
    lines = fp.readlines()
    for line in lines:
        parsed = json.loads(line)
        if 'AAPL' in parsed:
            parsed = parsed['AAPL']
            open_prices += [parsed['o']]
            close_prices += [parsed['c']]
            low_prices += [parsed['l']]
            high_prices += [parsed['h']]
            dates += [datetime.fromtimestamp(parsed['t'])]

fig = go.Figure(data=[go.Candlestick(x=dates,
                open=open_prices,
                high=high_prices,
                low=low_prices,
                close=close_prices)])

fig.show()