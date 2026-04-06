from nse_data import NSEDataFetcher
from data_pipeline import fetch_stock_data, build_features, build_targets
from model import train_model, predict_top_stocks
from notifier import EmailNotifier
import os


def format_results(results):
    top = results[['Stock', 'Buy_Prob']].head(5)

    message = "🔥 Top 5 Stocks for Tomorrow:\n\n"

    for _, row in top.iterrows():
        message += f"{row['Stock']} → {round(row['Buy_Prob'], 2)}\n"

    return message


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

    # -------------------------------
    # STEP 6: EMAIL NOTIFICATION
    # -------------------------------
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver = os.getenv("EMAIL_TO")

    print("DEBUG EMAIL USER:", sender)  # remove after testing

    notifier = EmailNotifier(sender, password)

    email_body = format_results(results)

    notifier.send_email(
        receiver,
        subject="📈 Daily Stock Recommendations",
        body=email_body
    )


if __name__ == "__main__":
    main()