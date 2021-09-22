from srv.validate import validate_choice, format_crypto
from srv.pricedata import get_all_symbols
from decouple import config
import finnhub

FINNHUB_CLIENT_KEY = config("FINNHUB_KEY")
FINNHUB_CLIENT = finnhub.Client(api_key=FINNHUB_CLIENT_KEY)


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


def complex_query(message, expected_responses):
    """
    Takes given message and expected responses to request
    multiple pieces of input from the user at once and validates
    them looking for the format "expected_response ticker"
    eg S AMC
    """
    while True:
        user_input = input(message)
        input_split = user_input.split()
        try:
            if len(input_split) != len(expected_responses):
                raise ValueError(
                    f"You must enter exactly {len(expected_responses)} "
                    "values separated by a space, "
                    f"you entered {len(input_split)}"
                )
        except ValueError as e:
            print(f"Invalid input: {e}")
        else:
            asset_type = input_split[0].upper()
            if validate_choice(asset_type, expected_responses):
                if asset_type == "S":
                    requested_ticker = input_split[1].upper()
                elif asset_type == "C":
                    requested_ticker = format_crypto(
                        input_split[1].upper()
                    )
                valid_tickers = get_all_symbols(
                    asset_type, FINNHUB_CLIENT
                )
                if validate_choice(requested_ticker, valid_tickers):
                    requested_ticker_list = [requested_ticker]
                    return asset_type, requested_ticker_list
