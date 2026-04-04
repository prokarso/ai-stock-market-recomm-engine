from nse_data import NSEDataFetcher
from data_pipeline import fetch_stock_data, build_features, build_targets
from model import train_model, predict_top_stocks


def main():
    print("🚀 Running Stock Recommendation Pipeline...")

    # Step 1: Get stocks
    fetcher = NSEDataFetcher()
    stocks = fetcher.get_nifty100()

    # Step 2: Fetch data
    data = fetch_stock_data(stocks)

    # Step 3: Features + targets
    data = build_features(data)
    data = build_targets(data)

    # Step 4: Train model
    features = ['Return_1d', 'Return_5d', 'MA_ratio', 'Momentum', 'Volatility']
    model = train_model(data, features)

    # Step 5: Predict
    results = predict_top_stocks(model, data, features)

    print("\n🔥 Top 5 Stocks for Tomorrow:\n")
    print(results[['Stock', 'Buy_Prob']].head(5))


if __name__ == "__main__":
    main()