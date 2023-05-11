# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import argparse

COINBASE_PRO_URL = "https://api.pro.coinbase.com/products/BTC-USD/book?level=2"
GEMINI_URL = "https://api.gemini.com/v1/book/btcusd"
KRAKEN_URL = "https://api.kraken.com/0/public/Depth?pair=XBTUSD"

def fetch_order_book(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch order book: {response.status_code}")
    return response.json()

def calculate_price_to_buy(order_book, amount_to_buy):
    bids = order_book.get('bids', [])
    remaining = amount_to_buy
    total_cost = 0

    for bid in bids:
        if isinstance(bid, dict):
            bid_price, bid_amount = float(bid.get('price', 0)), float(bid.get('amount', 0))
        else:
            bid_price, bid_amount = float(bid[0]), float(bid[1])
        amount_to_take = min(remaining, bid_amount)
        total_cost += amount_to_take * bid_price
        remaining -= amount_to_take
        if remaining <= 0:
            break

    return total_cost

def calculate_price_to_sell(order_book, amount_to_sell):
    asks = order_book.get('asks', [])
    remaining = amount_to_sell
    total_income = 0

    for ask in asks:
        if isinstance(ask, dict):
            ask_price, ask_amount = float(ask.get('price', 0)), float(ask.get('amount', 0))
        else:
            ask_price, ask_amount = float(ask[0]), float(ask[1])
        amount_to_take = min(remaining, ask_amount)
        total_income += amount_to_take * ask_price
        remaining -= amount_to_take
        if remaining <= 0:
            break

    return total_income


def main(amount_to_buy, amount_to_sell):
    # Fetch order book data
    coinbase_order_book = fetch_order_book(COINBASE_PRO_URL)
    gemini_order_book = fetch_order_book(GEMINI_URL)
    kraken_order_book = fetch_order_book(KRAKEN_URL)

    # Extract bids and asks from Kraken response
    kraken_bids = kraken_order_book['result']['XXBTZUSD']['bids']
    kraken_asks = kraken_order_book['result']['XXBTZUSD']['asks']
    kraken_order_book = {'bids': kraken_bids, 'asks': kraken_asks}

    # Calculate prices
    coinbase_buy_price = calculate_price_to_buy(coinbase_order_book, amount_to_buy)
    coinbase_sell_price = calculate_price_to_sell(coinbase_order_book, amount_to_sell)
    gemini_buy_price = calculate_price_to_buy(gemini_order_book, amount_to_buy)
    gemini_sell_price = calculate_price_to_sell(gemini_order_book, amount_to_sell)
    kraken_buy_price = calculate_price_to_buy(kraken_order_book, amount_to_buy)
    kraken_sell_price = calculate_price_to_sell(kraken_order_book, amount_to_sell)

    # Print results
    print(f"Coinbase Pro: Buy {amount_to_buy} BTC for ${coinbase_buy_price:.2f}, Sell {amount_to_sell} BTC for ${coinbase_sell_price:.2f}")
    print(f"Gemini: Buy {amount_to_buy} BTC for ${gemini_buy_price:.2f}, Sell {amount_to_sell} BTC for ${gemini_sell_price:.2f}")
    print(f"Kraken: Buy {amount_to_buy} BTC for ${kraken_buy_price:.2f}, Sell {amount_to_sell} BTC for ${kraken_sell_price:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch order books and calculate prices for buying and selling BTC")
    parser.add_argument('--buy', type=float, default=1, help='Amount of BTC to buy')
    parser.add_argument('--sell', type=float, default=1, help='Amount of BTC to sell')
    args = parser.parse_args()
    
    main(args.buy, args.sell)