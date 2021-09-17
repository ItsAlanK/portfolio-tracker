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


def convert_to_floats(lists):
    """
    Receives nested list and converts values into floats
    and replaces empty values with 0's
    """
    for list in lists:
        for index, value in enumerate(list):
            if value == "":
                list[index] = 0
            else:
                list[index] = float(list[index])
    return lists


def calculate_values(amounts, value):
    """
    Takes list of amounts of each asset held in portfolio worksheet
    and current value of each asset and calculates the total value of each
    asset held.
    """
    amounts = convert_to_floats(amounts)
    amounts_array = np.array(amounts)
    amount_totals = np.sum(amounts_array, 0)
    total_values = []
    for (amount, price) in zip(amount_totals, value):
        total_values.append(amount * price)
    return total_values
