def validate_choice(response, expected_response):
    """
    Check if response provided is valid.
    Raises error if response provided does not match an object
    in expected_response list.
    """
    try:
        if response.upper() not in expected_response:
            if len(expected_response) >= 5:
                expected_response = expected_response[:5]
                raise ValueError(
                    "Response must be a valid ticker symbol "
                    f"such as: {expected_response}"
                )
            raise ValueError(
                f"Response must be one of the following {expected_response}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True


def confirm_numbers(responses):
    """
    Confirms user provided 2 numbers.
    """
    if len(responses) == 2:
        try:
            for response in responses:
                response = float(response)
        except ValueError:
            print("Invalid data: your input must be numerical values.\n")
            return False
        else:
            return True
    else:
        print("Invalid data: you pust provide 2 numbers\n")
        return False
