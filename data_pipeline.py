import yfinance as yf
import pandas as pd


def fetch_stock_data(stocks):
    all_data = []

    for stock in stocks:
        try:
            df = yf.download(stock, period="6mo", interval="1d")

            if df.empty:
                continue

            # Clean columns
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df = df.loc[:, ~df.columns.duplicated()]
            df = df.reset_index()

            df['Stock'] = stock

            all_data.append(df)

        except:
            continue

    return pd.concat(all_data, ignore_index=True)


def build_features(data):
    data = data.sort_values(by=['Stock', 'Date'])

    data['Return_1d'] = data.groupby('Stock')['Close'].pct_change()
    data['Return_5d'] = data.groupby('Stock')['Close'].pct_change(5)

    data['MA_20'] = data.groupby('Stock')['Close'].transform(lambda x: x.rolling(20).mean())
    data['MA_50'] = data.groupby('Stock')['Close'].transform(lambda x: x.rolling(50).mean())

    data['MA_ratio'] = data['MA_20'] / data['MA_50']

    data['Momentum'] = data.groupby('Stock')['Close'].diff(5)
    data['Volatility'] = data.groupby('Stock')['Close'].transform(lambda x: x.rolling(20).std())

    return data


def build_targets(data):
    data['Target_Buy'] = (
        data.groupby('Stock')['Close'].shift(-1) > data['Close']
    ).astype(int)

    return data