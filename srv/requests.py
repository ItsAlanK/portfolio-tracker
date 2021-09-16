import finnhub
import env

FINNHUB_CLIENT = finnhub.Client(api_key=env.FINNHUB_KEY)


def get_live_data(ticker):
    print(FINNHUB_CLIENT.quote(ticker))
    print(ticker)


def get_all_symbols():
    """
    Generates a list of all valid stock tickers to
    validate user ticker selections
    """
    all_companies = FINNHUB_CLIENT.stock_symbols('US')
    symbols = []
    for company in all_companies:
        symbols.append(company["symbol"])
    return symbols
