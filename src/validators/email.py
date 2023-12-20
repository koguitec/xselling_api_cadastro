import re


def is_valid_email(email):
    """
    Validate the format of an email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    email_regex = re.compile(r'[^@]+@[^@]+\.[^@]+')
    return bool(re.match(email_regex, email))
