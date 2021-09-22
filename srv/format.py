from os import system, name


def format_crypto(tickers):
    """
    Takes list or string containing ticker informations
    and format it into form usable by finnhub;
    eg. BTC -> BINANCE:BTCUSDT
    """
    if type(tickers) is list:
        for i in range(len(tickers)):
            tickers[i] = "BINANCE:"\
                f"{tickers[i]}USDT"
    elif type(tickers) is str:
        tickers = f"BINANCE:{tickers}USDT"
    return tickers


def remove_crypto_format(tickers):
    """
    Removes formatting on crypto tickers used for finnhub,
    leaving basic ticker symbol for display purposes.
    """
    basic_tickers = [s.replace("BINANCE:", "") for s in tickers]
    basic_tickers_final = [s.replace("USDT", "") for s in basic_tickers]
    return basic_tickers_final


def clear():
    """
    Clears terminal when called.
    https://www.geeksforgeeks.org/clear-screen-python/
    """
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')
