from os import system, name


def validate_choice(response, expected_response):
    """
    Check if response provided is valid.
    Raises error if response provided does not match an object
    in expected_response list.
    """
    try:
        if response.upper() not in expected_response:
            if len(expected_response) >= 5:
                expected_response = expected_response[:5]
                raise ValueError(
                    "Response must be a valid ticker symbol "
                    f"such as: {expected_response}"
                )
            raise ValueError(
                f"Response must be one of the following {expected_response}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True


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
