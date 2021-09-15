def validate(response, expected_response):
    """
    Check if response provided is valid.
    Raises error if response provided does not match an object
    in expected_response list.
    """
    if response.upper() in expected_response:
        print("Valid Response")
    else:
        print("Invalid Response")