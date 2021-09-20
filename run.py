from srv import validate as val, pricedata, portfolio
import finnhub
import env

FINNHUB_CLIENT = finnhub.Client(api_key=env.FINNHUB_KEY)


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

    response = val.basic_input_request(message, expected_responses)

    if response == expected_responses[0]:
        live_search()
    elif response == expected_responses[1]:
        print("Obtaining position data...\n")
        portfolio_search()


def live_search():
    """
    Requests user input and confirms user inputs are valid.
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
                    requested_ticker = val.format_crypto(
                        search.split()[1].upper()
                    )
                valid_tickers = pricedata.get_all_symbols(
                    search_type, FINNHUB_CLIENT)
                if val.validate_choice(requested_ticker, valid_tickers):
                    break
    requested_ticker_list = [requested_ticker]
    live_price = pricedata.get_live_data(
        search_type, requested_ticker_list, FINNHUB_CLIENT)
    print(f"The current price for {requested_ticker} is ${live_price}\n")
    navigate()


def portfolio_search():
    """
    Searches portfolio worksheets and uses data to display live
    values for all assets held within portfolio.
    """
    all_portfolio_amounts = portfolio.retrieve_portfolio_amounts()

    stock_portfolio_tickers = all_portfolio_amounts[0][0]
    stock_amounts = all_portfolio_amounts[0][1:]
    stock_live_prices = pricedata.get_live_data(
        "S", stock_portfolio_tickers, FINNHUB_CLIENT)
    stock_values = portfolio.calculate_values(stock_amounts, stock_live_prices)
    print("Your current portfolio contains: ")

    crypto_portfolio_tickers = all_portfolio_amounts[1][0]
    val.format_crypto(crypto_portfolio_tickers)
    crypto_amounts = all_portfolio_amounts[1][1:]
    crypto_live_prices = pricedata.get_live_data(
        "C", crypto_portfolio_tickers, FINNHUB_CLIENT)
    crypto_values = portfolio.calculate_values(
        crypto_amounts, crypto_live_prices)
    crypto_tickers = val.remove_crypto_format(crypto_portfolio_tickers)

    print("Stock:")
    for (ticker, value) in zip(stock_portfolio_tickers, stock_values):
        print(f"{ticker} worth {value}")
    print("\n")
    print("Crypto:")
    for (ticker, value) in zip(crypto_tickers, crypto_values):
        print(f"{ticker} worth {value}")
    total_value = portfolio.calculate_total_value(stock_values, crypto_values)
    portfolio_options(total_value)


def portfolio_options(total_value):
    """
    Give user options for actions they can take to make changes
    ti their portfolio.
    """
    expected_responses = ["1", "2", "3", "4"]
    message = f"\nDo you want to: \n"\
        f"{expected_responses[0]} Create/Remove a position? \n"\
        f"{expected_responses[1]} Edit an existing position? \n"\
        f"{expected_responses[2]} Calculate current P/L? \n"\
        f"{expected_responses[3]} Return to start? \n"\

    response = val.basic_input_request(message, expected_responses)

    if response == expected_responses[0]:
        print("Creating new position...")
    elif response == expected_responses[1]:
        print("Editing a position...")
    elif response == expected_responses[2]:
        portfolio.calculate_pl(total_value)
    elif response == expected_responses[3]:
        start_program()


def navigate():
    """
    Give user option of searching another ticker or
    return to start menu options.
    """
    expected_responses = ["A", "B"]
    message = "If you wish to search another item "\
        f"press {expected_responses[0]} \n"\
        "If you wish to return to home "\
        f"press {expected_responses[1]}\n"

    response = val.basic_input_request(message, expected_responses)

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
