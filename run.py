import gspread
from google.oauth2.service_account import Credentials
import finnhub
import finnhubkey
from helpers import validate
import time

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("portfolio-tracker")
FINNHUB_CLIENT = finnhub.Client(api_key=finnhubkey.key)


def start_program():
    """
    Provide opening option to user
    """
    while True:
        expected_responses = ["L", "P"]
        print(f"If you would like to check Live Stock or Crypto prices press \
            {expected_responses[0]}.")
        print(f"If you would like to View or Edit your personal positions press \
            {expected_responses[1]}.")
        response = input(f"Enter your response \
            ({expected_responses[0]}/{expected_responses[1]}):\n")
        if validate(response, expected_responses):
            break


def main():
    """
    Run all program functions
    """
    start_program()


print("Welcome to your own personal Portfolio Tracker!\n")
time = int(time.time())
timelast = time - 60
print(FINNHUB_CLIENT.crypto_candles('BINANCE:DOGEUSDT', '1', timelast, time))
