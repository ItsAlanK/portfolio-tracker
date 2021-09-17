import finnhub
import env
import time

FINNHUB_CLIENT = finnhub.Client(api_key=env.FINNHUB_KEY)


def get_live_data(search_type, ticker):
    """
    Using params provided uses finnhub to fetch
    live price data and return it.
    """
    if search_type == "S":
        current_price = []
        for i in ticker:
            raw_data = FINNHUB_CLIENT.quote(i)
            current_price_raw = raw_data["c"]
            current_price.append(round(current_price_raw, 2))
        return current_price
    elif search_type == "C":
        time_end = round(time.time())
        time_start = time_end - 60
        raw_data = FINNHUB_CLIENT.crypto_candles(
            ticker, 1, time_start, time_end
            )
        current_price_raw = raw_data["c"]
        current_price = round(current_price_raw[0], 2)
        return current_price


def get_all_symbols(type):
    """
    Generates a list of all valid stock tickers to
    validate user ticker selections.
    """
    if type == "S":
        all_tickers = FINNHUB_CLIENT.stock_symbols('US')
    elif type == "C":
        all_tickers = FINNHUB_CLIENT.crypto_symbols('BINANCE')
    symbols = []
    for ticker in all_tickers:
        symbols.append(ticker["symbol"])
    return symbols
