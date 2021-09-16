import gspread
from google.oauth2.service_account import Credentials
from srv import validate, requests

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("portfolio-tracker")


def start_program():
    """
    Provide opening option to user and runs appropriate
    function based on the response given.
    """
    while True:
        expected_responses = ["L", "P"]
        print(
            "If you would like to check Live Stock or "
            f"Crypto prices press {expected_responses[0]}."
        )
        print(
            "If you would like to View or Edit your personal positions "
            f"press {expected_responses[1]}."
        )
        response = input(
            "Enter your response "
            f"({expected_responses[0]}/{expected_responses[1]}):\n"
            ).upper()

        if validate.validate_choice(response, expected_responses):
            break

    if response == expected_responses[0]:
        live_search()
    elif response == expected_responses[1]:
        print("Obtaining position data")


def live_search():
    """
    Takes user's request and provides market data for the given ticker.
    """
    while True:
        expected_search_types = ["C", "S"]
        search = input(
                f"Enter {expected_search_types[0]} if you wish to search a "
                f"cryptocurrency or {expected_search_types[1]} for "
                "a stock\nfollowed by the ticker/symbol you wish to view, "
                "separated with a space (eg S AMC): \n"
                )
        search_type = search.split()[0].upper()
        requested_ticker = search.split()[1].upper()
        valid_tickers = requests.get_all_symbols()
        if validate.validate_choice(search_type, expected_search_types) \
                and validate.validate_choice(requested_ticker, valid_tickers):
            break

    live_price = requests.get_live_data(requested_ticker)
    print(f"The current price for {requested_ticker} is ${live_price}\n")
    navigate()


def navigate():
    while True:
        expected_responses = ["A", "B"]
        response = input(
                    "If you wish to search another item "
                    f"press {expected_responses[0]} "
                    "If you wish to return to home "
                    f"press {expected_responses[1]}\n"
                    ).upper()
        if validate.validate_choice(response, expected_responses):
            break
    if response == expected_responses[0]:
        live_search()
    elif response == expected_responses[1]:
        start_program()


def main():
    """
    Run all program functions
    """
    start_program()


print("Welcome to your own personal Portfolio Tracker!\n")
main()


# time = int(time.time())
# timelast = time - 60
# print(FINNHUB_CLIENT.crypto_candles('BINANCE:DOGEUSDT', '1', timelast, time))
