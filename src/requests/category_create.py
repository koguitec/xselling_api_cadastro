"""Module for structured category requests objects"""
import uuid
from typing import Dict

from .validation.invalid_request import InvalidRequest
from .validation.valid_request import ValidRequest


def build_create_category_request(category: Dict):
    """Factory for requests

    Args:
        category (dict): Dictionary containing category data

    Returns:
        Object: Return InvalidRequest if errors, otherwise, returns ValidRequest
    """
    invalid_req = InvalidRequest()

    if not isinstance(category['client_id'], int):
        invalid_req.add_error('value', 'client id must be an integer')

    if invalid_req.has_errors():
        return invalid_req

    return ValidRequest(data=category)
