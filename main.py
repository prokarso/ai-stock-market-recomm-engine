from nse_data import NSEDataFetcher
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Create object
fetcher = NSEDataFetcher()

# Fetch stocks
stocks = fetcher.get_nifty100()

print("First 10 stocks:", stocks[:10])
print("Total:", len(stocks))

# Save to CSV
fetcher.save_to_csv(stocks)

all_data = []

for stock in stocks:
    try:
        df = yf.download(stock, period="6mo", interval="1d")

        if df.empty:
            print(f"⚠️ No data for {stock}")
            continue

        # ✅ Fix 1: Flatten multi-index columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # ✅ Fix 2: Remove duplicate columns
        df = df.loc[:, ~df.columns.duplicated()]

        # ✅ Fix 3: Reset index properly
        df = df.reset_index()

        # ✅ Add stock column
        df['Stock'] = stock

        all_data.append(df)

    except Exception as e:
        print(f"❌ Error fetching {stock}: {e}")

data = pd.concat(all_data, ignore_index=True)
data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]

data = data.sort_values(by=['Stock', 'Date'])

data['Return_1d'] = data.groupby('Stock')['Close'].pct_change()
data['Return_5d'] = data.groupby('Stock')['Close'].pct_change(5)

data['MA_20'] = data.groupby('Stock')['Close'].transform(lambda x: x.rolling(20).mean())
data['MA_50'] = data.groupby('Stock')['Close'].transform(lambda x: x.rolling(50).mean())

data['MA_ratio'] = data['MA_20'] / data['MA_50']

data['Momentum'] = data.groupby('Stock')['Close'].diff(5)

data['Volatility'] = data.groupby('Stock')['Close'].transform(lambda x: x.rolling(20).std())

print(data.head())
print(data.shape)
data['Target_Buy'] = (data.groupby('Stock')['Close'].shift(-1) > data['Close']).astype(int)
data['Target_Sell'] = (data.groupby('Stock')['Close'].shift(-1) < data['Close']).astype(int)
features = ['Return_1d', 'Return_5d', 'MA_ratio', 'Momentum', 'Volatility']

# Select only required columns
model_data = data[features + ['Target_Buy']].copy()

# Drop rows with ANY NaN
model_data = model_data.dropna()

# Split again
X = model_data[features]
y = model_data['Target_Buy']

print(X.head())
print(y.head())



X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)



model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print("Model Accuracy:", accuracy)