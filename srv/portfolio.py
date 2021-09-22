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


def assign_sheets_type(type):
    """
    Assigns correct pari of sheets, either crypto or stock
    depending on type in params.
    """
    if type == "S":
        amount_sheet = SHEET.worksheet("stock-amounts")
        price_sheet = SHEET.worksheet("stock-pos-prices")
    elif type == "C":
        amount_sheet = SHEET.worksheet("crypto-amounts")
        price_sheet = SHEET.worksheet("crypto-pos-prices")
    return amount_sheet, price_sheet


def check_positions_present(type, ticker, amount_sheet, price_sheet):
    """
    Confirms requested ticker is present in worksheet.
    """
    try:
        if (ticker not in amount_sheet and
                ticker not in price_sheet):
            raise ValueError(
                "The ticker you've chosen is not present in portfolio"
            )
    except ValueError as e:
        print(f"{e}")
        return False
    else:
        return True


def create_position(type, ticker):
    """
    If ticker provided is not present in portfolio, ticker will
    be added with data input by user. If ticker is present in
    portfolio ticker will be removed.
    """
    amount_sheet = assign_sheets_type(type)[0]
    price_sheet = assign_sheets_type(type)[1]
    ticker = ticker.pop()
    amount_sheet_tickers = amount_sheet.get_all_values()[0]
    price_sheet_tickers = price_sheet.get_all_values()[0]
    if check_positions_present(
            type, ticker, amount_sheet_tickers, price_sheet_tickers):
        print(f"Removing {ticker} from your portfolio.")
        column = amount_sheet.find(ticker).col
        amount_sheet.delete_columns(column)
        price_sheet.delete_columns(column)
    else:
        print(f"Adding {ticker} to your portfolio")
        data = input(
            f"\nPlease enter the amount of {ticker} you wish to add "
            "followed by the price you purchased it at\n"
            "eg. '5 500'\n")
        amount = data.split()[0]
        price = data.split()[1]
        print("Updating portfolio...")
        row = 1
        column = next_available_column(amount_sheet, row)
        amount_sheet.update_cell(row, column, ticker)
        amount_sheet.update_cell(row + 1, column, amount)
        price_sheet.update_cell(row, column, ticker)
        price_sheet.update_cell(row + 1, column, price)
        print(f"Added {amount} {ticker} at {price} to your portfolio\n")


def edit_positions(type, ticker):
    """
    Edits worksheet info for desired asset with info provided
    by the user.
    """
    amount_sheet = assign_sheets_type(type)[0]
    price_sheet = assign_sheets_type(type)[1]
    ticker = ticker.pop()
    amount_sheet_tickers = amount_sheet.get_all_values()[0]
    price_sheet_tickers = price_sheet.get_all_values()[0]
    if check_positions_present(
            type, ticker, amount_sheet_tickers, price_sheet_tickers):
        data = input(
            f"\nPlease enter the amount of {ticker} you purchased/sold "
            "(using '-' to indicate a sale) "
            "followed by the price you purchased it at\n"
            "eg. '5 500' or '-10 25'\n")
        amount = data.split()[0]
        price = data.split()[1]
        print("Updating portfolio...")
        column = amount_sheet.find(ticker).col
        row = next_available_row(amount_sheet, column)
        amount_sheet.update_cell(row, column, amount)
        price_sheet.update_cell(row, column, price)
        print(f"{amount} {ticker} at ${price} added to portfolio")
    else:
        print("Not present in file")


def next_available_row(worksheet, column):
    """
    Finds next empty row of column provided for a worksheet and returns
    row value.
    https://bit.ly/3ApiyzI
    """
    str_list = list(filter(None, worksheet.col_values(column)))
    return str(len(str_list)+1)


def next_available_column(worksheet, row):
    """
    Finds next empty column of row provided for a worksheet and returns
    column value.
    """
    str_list = list(filter(None, worksheet.row_values(row)))
    return str(len(str_list)+1)


def calculate_total_buyin(prices, amounts):
    """
    Takes lists of prices and amounts of assets at each buyin value
    to calculate money spent on assets.
    Replaces any negative amounts with zero as these
    are realised gains/losses.
    """
    buy_prices = convert_to_floats(prices[1:])
    for (list, price) in zip(amounts, buy_prices):
        for i in range(len(list)):
            if list[i] < 0:
                price[i] *= 0
    buy_values = np.multiply(buy_prices, amounts)
    buy_totals = np.sum(buy_values)
    return buy_totals


def calculate_realised(prices, amounts):
    """
    Takes lists of prices and amounts of assets at each buyin value
    and uses negative amounts as a marker for assets sold.
    These amounts' values are calculated and returned.
    """
    buy_prices = convert_to_floats(prices[1:])
    realised_profits = []
    for (list, price) in zip(amounts, buy_prices):
        for i in range(len(list)):
            if list[i] < 0:
                list[i] *= -1
                realised_profits.append(list[i] * price[i])
    realised_total = np.sum(realised_profits)
    return realised_total


def calculate_pl(total_value, stock_amounts, crypto_amounts):
    """
    Displays P/L of portfolio by calculating money spent on assets
    and comparing it to total_value of the portfolio currently.
    """
    stock_buyin_raw = SHEET.worksheet("stock-pos-prices").get_all_values()
    crypto_buyin_raw = SHEET.worksheet("crypto-pos-prices").get_all_values()
    stock_raw = SHEET.worksheet("stock-pos-prices").get_all_values()
    crypto_raw = SHEET.worksheet("crypto-pos-prices").get_all_values()

    buy_totals_stock = calculate_total_buyin(stock_buyin_raw, stock_amounts)
    buy_totals_crypto = calculate_total_buyin(crypto_buyin_raw, crypto_amounts)
    realised_profit_stock = calculate_realised(stock_raw, stock_amounts)
    realised_profit_crypto = calculate_realised(crypto_raw, crypto_amounts)
    total_spent = round(buy_totals_stock + buy_totals_crypto, 2)
    total_value_realised = (
        total_value + realised_profit_stock + realised_profit_crypto)
    total_pl = round(total_value_realised - total_spent, 2)

    print(f"\nThe total amount spent on your portfolio is: ${total_spent}")
    print(f"The current total value of your portfolio is: ${total_value}\n")
    print(f"Your current P/L is: ${total_pl}")
