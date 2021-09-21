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
        total_values.append(round(amount * price, 2))
    return total_values


def calculate_total_value(stock_values, crypto_values):
    """
    Takes lists of total values for stock and crypto and returns
    their sum.
    """
    stock_total = np.sum(stock_values)
    crypto_total = np.sum(crypto_values)
    return round(stock_total + crypto_total, 2)


def calculate_total_buyin(prices, amounts):
    """
    Takes lists of prices and amounts of assets at each buyin value
    to calculate money spent on assets.
    """
    buy_prices = convert_to_floats(prices[1:])
    buy_values = np.multiply(buy_prices, amounts)
    buy_totals = np.sum(buy_values)
    return buy_totals


def calculate_pl(total_value, stock_amounts, crypto_amounts):
    """
    Displays P/L of portfolio by calculating money spent on assets
    and comparing it to total_value of the portfolio currently.
    """
    stock_buyin_raw = SHEET.worksheet("stock-pos-prices").get_all_values()
    crypto_buyin_raw = SHEET.worksheet("crypto-pos-prices").get_all_values()

    buy_totals_stock = calculate_total_buyin(stock_buyin_raw, stock_amounts)
    buy_totals_crypto = calculate_total_buyin(crypto_buyin_raw, crypto_amounts)
    total_spent = round(buy_totals_stock + buy_totals_crypto, 2)
    total_pl = round(total_value - total_spent, 2)

    print(f"\nThe total amount spent on your portfolio is: ${total_spent}")
    print(f"The current total value of your portfolio is: ${total_value}\n")
    print(f"Your current P/L is: ${total_pl}")


def edit_positions(type, ticker):
    """
    Edits worksheet info for desired asset with info provided
    by the user.
    """
    if type == "S":
        amount_sheet = SHEET.worksheet("stock-amounts")
        price_sheet = SHEET.worksheet("stock-pos-prices")
    elif type == "C":
        amount_sheet = SHEET.worksheet("crypto-amounts")
        price_sheet = SHEET.worksheet("crypto-pos-prices")
