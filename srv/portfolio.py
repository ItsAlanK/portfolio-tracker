import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("portfolio-tracker")


def retrieve_portfolio_amounts():
    """
    Retrieve and parse position data from google sheets.
    """
    stock_amounts_raw = SHEET.worksheet("stock-amounts").get_all_values()
    crypto_amounts_raw = SHEET.worksheet("crypto-amounts").get_all_values()
    return stock_amounts_raw, crypto_amounts_raw
