def validate_choice(response, expected_response):
    """
    Check if response provided is valid.
    Raises error if response provided does not match an object
    in expected_response list.
    """
    try:
        if response.upper() not in expected_response:
            raise ValueError(
                f"Response must be one of the following {expected_response}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True


def basic_input_request(message, expected_responses):
    """
    Takes a message and expected responses to create a
    basic input request and validate responses against
    expected_responses.
    """
    while True:
        response = input(message).upper()
        if validate_choice(response, expected_responses):
            break
    return response
