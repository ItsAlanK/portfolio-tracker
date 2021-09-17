import gspread
from google.oauth2.service_account import Credentials
import numpy as np


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


def convert_to_floats(list):
    """
    Receives nested list and converts values into floats
    and replaces empty values with 0's
    """
    for i in list:
        for index, item in enumerate(i):
            if item == "":
                i[index] = 0
            else:
                i[index] = float(i[index])
    return list


def calculate_values(amounts, value):
    amounts = convert_to_floats(amounts)
    amounts_array = np.array(amounts)
    print(amounts_array)
