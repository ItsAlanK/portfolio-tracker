import gspread
from google.oauth2.service_account import Credentials
from srv import validate as val, requests

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
    expected_responses = ["L", "P"]
    message = "If you would like to check Live Stock or "\
        f"Crypto prices press {expected_responses[0]}. "\
        "If you would like to View or Edit your personal positions "\
        f"press {expected_responses[1]}.\n"\
        "Enter your response "\
        f"({expected_responses[0]}/{expected_responses[1]}):\n"

    response = requests.basic_input_request(message, expected_responses)

    if response == expected_responses[0]:
        live_search()
    elif response == expected_responses[1]:
        print("Obtaining position data")


def live_search():
    """
    Confirms user inputs are valid.
    Formats ticker for crypto if c is chosen.
    Takes user's inputs and provides market data for the given ticker.
    """
    while True:
        expected_search_types = ["C", "S"]
        search = input(
                f"Enter {expected_search_types[0]} if you wish to search a "
                f"cryptocurrency or {expected_search_types[1]} for "
                "a stock\nfollowed by the ticker/crypto symbol "
                "combo you wish to view, separated with "
                "a space (eg S AMC, C BTC): \n"
                )
        search_split = search.split()
        try:
            if len(search_split) != 2:
                raise ValueError(
                    "You must enter exactly 2 values separated by a space, "
                    f"you entered {len(search_split)}"
                )
        except ValueError as e:
            print(f"Invalid input: {e}")
        else:
            search_type = search_split[0].upper()
            if val.validate_choice(search_type, expected_search_types):
                if search_type == "S":
                    requested_ticker = search.split()[1].upper()
                elif search_type == "C":
                    requested_ticker = "BINANCE:"\
                        f"{search.split()[1].upper()}USDT"
                valid_tickers = requests.get_all_symbols(search_type)
                if val.validate_choice(requested_ticker, valid_tickers):
                    break

    live_price = requests.get_live_data(search_type, requested_ticker)
    print(f"The current price for {requested_ticker} is ${live_price}\n")
    navigate()


def navigate():
    expected_responses = ["A", "B"]
    message = "If you wish to search another item "\
        f"press {expected_responses[0]} \n"\
        "If you wish to return to home "\
        f"press {expected_responses[1]}\n"

    response = requests.basic_input_request(message, expected_responses)

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
