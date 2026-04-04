import requests
import pandas as pd
import json


class NSEDataFetcher:

    def __init__(self):
        self.base_url = "https://www.nseindia.com"
        self.api_url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20100"

        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br"
        }

        self.session = requests.Session()

    # -------------------------------
    # PRIMARY: Fetch from NSE API
    # -------------------------------
    def fetch_from_nse(self):
        try:
            # Warm-up request
            self.session.get(self.base_url, headers=self.headers)

            headers = self.headers.copy()
            headers["Referer"] = self.base_url

            response = self.session.get(self.api_url, headers=headers)

            if response.status_code != 200:
                print(f"❌ NSE failed with status {response.status_code}")
                return []

            data = response.json()

            stocks = [item['symbol'] + ".NS" for item in data['data']]

            print("✅ Fetched from NSE API")
            return stocks

        except Exception as e:
            print("❌ NSE fetch error:", e)
            return []

    # -------------------------------
    # FALLBACK 1: Load from JSON
    # -------------------------------
    def load_from_json(self, filepath="nifty100.json"):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            stocks = [item['symbol'] + ".NS" for item in data['data']]

            print("✅ Loaded from local JSON")
            return stocks

        except Exception as e:
            print("❌ JSON load error:", e)
            return []

    # -------------------------------
    # FALLBACK 2: Static list
    # -------------------------------
    def fallback_static_list(self):
        print("⚠️ Using static fallback list")

        return [
            "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
            "ICICIBANK.NS", "SBIN.NS", "LT.NS", "ITC.NS",
            "HINDUNILVR.NS", "KOTAKBANK.NS"
        ]

    # -------------------------------
    # MASTER METHOD (USE THIS)
    # -------------------------------
    def get_nifty100(self, json_path="nifty100.json"):

        # Step 1: Try NSE
        stocks = self.fetch_from_nse()

        # Step 2: Fallback to JSON
        if len(stocks) == 0:
            print("🔁 Falling back to JSON...")
            stocks = self.load_from_json(json_path)

        # Step 3: Final fallback
        if len(stocks) == 0:
            print("🔁 Falling back to static list...")
            stocks = self.fallback_static_list()

        return stocks

    # -------------------------------
    # SAVE UTILITY
    # -------------------------------
    def save_to_csv(self, stocks, filename="ind_nifty100list.csv"):
        df = pd.DataFrame(stocks, columns=["Symbol"])
        df.to_csv(filename, index=False)
        print(f"💾 Saved {len(stocks)} stocks to {filename}")