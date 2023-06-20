import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta

import math
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler


# Binance API credentials
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

# Initialize Binance client
client = Client("TZOv9X5b1Upa1NInNjoISwaPYYNlttYEIo5jtg0LPiYae7QGjZzkEP9LONYFNl5m", "XXwWMpzPBbsoKRWg1AeojG3nndxPZtAwmRlUyexyR3ft7a1qsdfXfBqzReFTZ8cw",  tld='com')

# Define the symbol and interval
symbol = 'BTCUSDT'
interval = Client.KLINE_INTERVAL_1HOUR

# Calculate the start and end dates for the last month
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Convert dates to milliseconds (required by Binance API)
start_timestamp = int(start_date.timestamp() * 1000)
end_timestamp = int(end_date.timestamp() * 1000)

# Retrieve Klines data from Binance
klines = client.futures_klines(symbol=symbol, interval=interval, startTime=start_timestamp, endTime=end_timestamp)

# Define the column names for the dataframe
columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
           'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']

# Create a dataframe from the Klines data
df = pd.DataFrame(klines, columns=columns)

# Convert timestamps to datetime format
df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')

# Convert numeric columns to float
numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote asset volume', 'Taker buy base asset volume',
                   'Taker buy quote asset volume']
df[numeric_columns] = df[numeric_columns].astype(float)


data=df.filter(['Close'])
dataset=data.values
training_data_len=math.ceil(len(dataset)*0.8) # setting training data to be 80% of the whole data



# Print the dataframe
print(training_data_len)
