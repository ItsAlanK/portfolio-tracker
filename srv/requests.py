import finnhub
import env

FINNHUB_CLIENT = finnhub.Client(api_key=env.FINNHUB_KEY)


def get_live_data(ticker):
    print(FINNHUB_CLIENT.quote(ticker))
    print(ticker)


def get_all_symbols():
    all_companies = FINNHUB_CLIENT.stock_symbols('US')
    symbols = []
    for company in all_companies:
        symbols.append(company["symbol"])
    print(symbols)
