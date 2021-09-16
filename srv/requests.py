import finnhub
import env

FINNHUB_CLIENT = finnhub.Client(api_key=env.FINNHUB_KEY)


def get_live_data(ticker):
    print(FINNHUB_CLIENT.quote(ticker))
