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


def basic_input_request(message, expected_responses):
    """
    Takes a message and expected responses to create a
    basic input request and validate responses against
    expected_responses.
    """
    while True:
        response = input(message).upper()
        if validate_choice(response, expected_responses):
            break
    return response


def format_crypto(tickers):
    if type(tickers) is list:
        for i in range(len(tickers)):
            tickers[i] = "BINANCE:"\
                f"{tickers[i]}USDT"
    elif type(tickers) is str:
        tickers = f"BINANCE:{tickers}USDT"
    return tickers
