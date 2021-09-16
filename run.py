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
    search = input(
            "Enter 'C' is you wish to search a cryptocurrency or 'S' "
            "for a stock followed by the ticker/symbol you wish to view: \n"
            )
    search_type_options = ["C", "S"]
    search_type = search.split()[0].upper()
    if validate.validate_choice(search_type, search_type_options):
        # requests.get_live_data(search)
        print(search)
    else:
        requests.get_all_symbols()


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
