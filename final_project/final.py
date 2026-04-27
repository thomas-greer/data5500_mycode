import os
import json
import requests
import pandas as pd
from datetime import datetime
import time

STOCKS = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META", "NFLX", "AMD", "SPY"]

DATA_FOLDER = "/home/ubuntu/data5500_mycode/final_project/data"
RESULTS_FILE = "/home/ubuntu/data5500_mycode/final_project/results/results.json"

ALPHA_VANTAGE_API_KEY = "XSND8DNR3W741FS2"

ALPACA_API_KEY = "PK2DRULC52ISFRUC3GMISABLW6"
ALPACA_SECRET_KEY = "5rqbx5n6QXUAEaC6MdDnjvhpYkN3S9e5zoRWnwqwZRQJ"

# IMPORTANT: must include "paper"
ALPACA_BASE_URL = "https://paper-api.alpaca.markets"


def get_stock_data(symbol):
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "outputsize": "compact"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "Time Series (Daily)" not in data:
        print(f"Could not get data for {symbol}")
        print(data)
        return None

    daily_data = data["Time Series (Daily)"]

    rows = []

    for date, values in daily_data.items():
        rows.append({
            "date": date,
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"]),
            "volume": int(values["5. volume"])
        })

    df = pd.DataFrame(rows)
    df = df.sort_values("date")

    return df

def save_stock_csv(symbol, new_df):
    filepath = f"{DATA_FOLDER}/{symbol}.csv"

    if os.path.exists(filepath):
        old_df = pd.read_csv(filepath)

        combined_df = pd.concat([old_df, new_df])
        combined_df = combined_df.drop_duplicates(subset=["date"])
        combined_df = combined_df.sort_values("date")
    else:
        combined_df = new_df

    combined_df.to_csv(filepath, index=False)

    return combined_df

def sma_crossover_strategy(df):
    df = df.copy()

    df["sma_short"] = df["close"].rolling(window=5).mean()
    df["sma_long"] = df["close"].rolling(window=20).mean()

    buy_price = None
    sell_price = None
    profit = 0
    last_signal = "hold"

    for i in range(20, len(df)):
        yesterday_short = df.iloc[i - 1]["sma_short"]
        yesterday_long = df.iloc[i - 1]["sma_long"]

        today_short = df.iloc[i]["sma_short"]
        today_long = df.iloc[i]["sma_long"]

        today_price = df.iloc[i]["close"]

        #buy
        if yesterday_short <= yesterday_long and today_short > today_long:
            last_signal = "buy"

            if sell_price is not None:
                profit += sell_price - today_price
                sell_price = None
            buy_price = today_price

        #sell
        elif yesterday_short >= yesterday_long and today_short < today_long:
            last_signal = "sell"

            if buy_price is not None:
                profit += today_price - buy_price
                buy_price = None

            #short selling
            sell_price = today_price

    return profit, last_signal

def mean_reversion_strategy(df):
    df = df.copy()

    df["average"] = df["close"].rolling(window=20).mean()

    buy_price = None
    sell_price = None
    profit = 0
    last_signal = "hold"

    for i in range(20, len(df)):
        price = df.iloc[i]["close"]
        average = df.iloc[i]["average"]

        # buy parameter
        if price < average * 0.95:
            last_signal = "buy"

            if sell_price is not None:
                profit += sell_price - price
                sell_price = None

            buy_price = price

        # sell parameter
        elif price > average * 1.05:
            last_signal = "sell"

            if buy_price is not None:
                profit += price - buy_price
                buy_price = None

            sell_price = price

    return profit, last_signal

def momentum_strategy(df):
    df = df.copy()

    buy_price = None
    sell_price = None
    profit = 0
    last_signal = "hold"

    for i in range(5, len(df)):
        today_price = df.iloc[i]["close"]
        old_price = df.iloc[i - 5]["close"]

        percent_change = (today_price - old_price) / old_price

        # buy parameter
        if percent_change > 0.03:
            last_signal = "buy"

            if sell_price is not None:
                profit += sell_price - today_price
                sell_price = None

            buy_price = today_price

        # sell parameter
        elif percent_change < -0.03:
            last_signal = "sell"

            if buy_price is not None:
                profit += today_price - buy_price
                buy_price = None

            sell_price = today_price

    return profit, last_signal

def submit_paper_order(symbol, signal):

    if signal not in ["buy", "sell"]:
        return

    url = f"{ALPACA_BASE_URL}/v2/orders"

    headers = {
        "APCA-API-KEY-ID": ALPACA_API_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
    }

    order = {
        "symbol": symbol,
        "qty": 1,
        "side": signal,
        "type": "market",
        "time_in_force": "day"
    }

    response = requests.post(url, json=order, headers=headers)

    print(f"Submitted paper {signal} order for {symbol}")
    print(response.text)

def main():
    all_results = []

    best_profit = None
    best_stock = None
    best_strategy = None

    strategies = {
        "SMA Crossover": sma_crossover_strategy,
        "Mean Reversion": mean_reversion_strategy,
        "Momentum": momentum_strategy
    }

    for stock in STOCKS:
        print(f"\nWorking on {stock}...")

        time.sleep(5)

        new_data = get_stock_data(stock)

        if new_data is None:
            continue

        df = save_stock_csv(stock, new_data)

        for strategy_name, strategy_function in strategies.items():
            profit, last_signal = strategy_function(df)

            result = {
                "stock": stock,
                "strategy": strategy_name,
                "profit": round(profit, 2),
                "last_signal": last_signal
            }

            all_results.append(result)

            print(f"{stock} | {strategy_name} | Profit: ${profit:.2f} | Signal: {last_signal}")

            if last_signal in ["buy", "sell"]:
                print(f"You should {last_signal} {stock} today using {strategy_name}")

                # submitting paper
                if strategy_name == "SMA Crossover":
                    submit_paper_order(stock, last_signal)

            if best_profit is None or profit > best_profit:
                best_profit = profit
                best_stock = stock
                best_strategy = strategy_name

    final_results = {
        "date_ran": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "best_result": {
            "stock": best_stock,
            "strategy": best_strategy,
            "profit": round(best_profit, 2)
        },
        "all_results": all_results
    }

    with open(RESULTS_FILE, "w") as file:
        json.dump(final_results, file, indent=4)

    print("\nSaved results to results.json")
    print(f"Best result: {best_stock} using {best_strategy} made ${best_profit:.2f}")



main()