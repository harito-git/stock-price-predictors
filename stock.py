import requests
import time
from model import StockModel
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

import os
load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
#API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
class Stock:
    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.price = None
        self.prices = []
        self.model = StockModel()
        self.history = []
        self.last_updated = 0
        self.prediction = None

    def fetch_data(self):
        # Cache for 60 seconds
        ticker = yf.Ticker(self.symbol)
        hist = ticker.history(period="1mo")  # or whatever you prefer
        self.price = ticker.info.get('regularMarketPrice')
        self.prices = hist['Close'].tolist()
        print(self.prices)
        if not self.prices:
            raise Exception(f"No price data available for symbol {self.symbol}")
        self.history = [{"date": str(date.date()), "price": row["Close"]} for date, row in hist.iterrows()]
        model = ARIMA(self.prices, order=(1, 0, 1))
        model_fit = model.fit()

        # Forecast future prices (not differences)
        forecast_steps = 5  # predict future stock prices for 5 future days, steps is number of days
        forecast = model_fit.forecast(steps=forecast_steps)
        self.prediction = forecast.tolist()
        self.last_updated = time.time()
        
        """
        if time.time() - self.last_updated < 60:
            return

        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": self.symbol,
            "interval": "5min",
            "apikey": ALPHA_VANTAGE_API_KEY,
        }
        r = requests.get(ALPHA_VANTAGE_URL, params=params)
        data = r.json()
        series = data.get("Time Series (5min)")
        if not series:
            raise Exception(f"No data for symbol {self.symbol}")

        self.history = [
            {"time": t, "price": float(info["4. close"])}
            for t, info in sorted(series.items())
        ]
        self.price = self.history[-1]["price"]
        self.last_updated = time.time()
        """

class StockTracker:
    def __init__(self):
        self.stocks = {}
        self.model = StockModel()

    def get_stock(self, symbol):
        symbol = symbol.upper()
        if symbol not in self.stocks:
            self.stocks[symbol] = Stock(symbol)
        stock = self.stocks[symbol]
        stock.fetch_data()
        return stock

