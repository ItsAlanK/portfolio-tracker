import time


def get_live_data(search_type, ticker, client):
    """
    Using params provided uses finnhub to fetch
    live price data and return it.
    """
    if search_type == "S":
        current_price = []
        for asset in ticker:
            raw_data = client.quote(asset)
            current_price_raw = raw_data["c"]
            current_price.append(round(current_price_raw, 2))
        return current_price
    elif search_type == "C":
        current_price = []
        time_end = round(time.time())
        time_start = time_end - 60
        for asset in ticker:
            asset = f"BINANCE:{asset}USDT"
            raw_data = client.crypto_candles(
                asset, 1, time_start, time_end
                )
            current_price_raw = raw_data["c"]
            current_price.append(round(current_price_raw[0], 2))
        return current_price


def get_all_symbols(type, client):
    """
    Generates a list of all valid stock tickers to
    validate user ticker selections.
    """
    if type == "S":
        all_tickers = client.stock_symbols('US')
    elif type == "C":
        all_tickers = client.crypto_symbols('BINANCE')
    symbols = []
    for ticker in all_tickers:
        symbols.append(ticker["symbol"])
    return symbols
