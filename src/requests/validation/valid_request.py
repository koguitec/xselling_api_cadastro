"""Module for the valid request type"""


class ValidRequest:
    """ClientListValidRequest"""

    def __init__(self, *, data=None, filters=None):
        self.data = data
        self.filters = filters

    def __bool__(self):
        return True
