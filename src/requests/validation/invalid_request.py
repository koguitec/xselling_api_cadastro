"""Module for the invalid request type"""


class InvalidRequest:
    """ClientListInvalidRequest"""

    def __init__(self):
        self.errors = []

    def add_error(self, parameter, message):
        """Add request errors if they exists

        Args:
            parameter (str): Type of error found in the request
            message (str): Descript of the error that ocurred

        Returns:
            None: This function has no return
        """
        self.errors.append({'parameter': parameter, 'message': message})

    def has_errors(self):
        """Checks wether an error exists

        Returns:
            Bool: Boolen filed signaling the existance of errors
        """
        return len(self.errors) > 0

    def __bool__(self):
        return False
