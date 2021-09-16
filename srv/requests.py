import finnhub
import env
from srv import validate
import time

FINNHUB_CLIENT = finnhub.Client(api_key=env.FINNHUB_KEY)


def basic_input_request(message, expected_responses):
    while True:
        response = input(message).upper()
        if validate.validate_choice(response, expected_responses):
            break
    return response


def get_live_data(search_type, ticker):
    if search_type == "S":
        raw_data = FINNHUB_CLIENT.quote(ticker)
        current_price_raw = raw_data["c"]
        current_price = round(current_price_raw, 2)
        return current_price
    elif search_type == "C":
        time_end = round(time.time())
        time_start = time_end - 60
        raw_data = FINNHUB_CLIENT.crypto_candles(ticker, 1, time_start, time_end)
        current_price_raw = raw_data["c"]
        current_price = round(current_price_raw[0], 2)
        return current_price


def get_all_symbols(type):
    """
    Generates a list of all valid stock tickers to
    validate user ticker selections
    """
    if type == "S":
        all_tickers = FINNHUB_CLIENT.stock_symbols('US')
    elif type == "C":
        all_tickers = FINNHUB_CLIENT.crypto_symbols('BINANCE')
    symbols = []
    for ticker in all_tickers:
        symbols.append(ticker["symbol"])
    return symbols
