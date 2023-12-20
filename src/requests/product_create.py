import uuid
from typing import Dict

from src.requests.validation.invalid_request import InvalidRequest
from src.requests.validation.valid_request import ValidRequest


def build_create_product_request(product: Dict):
    """Factory for requests

    Args:
        product (dict): Dictionary containing product data

    Returns:
        Object: Return InvalidRequest if errors, otherwise, returns ValidRequest
    """
    invalid_req = InvalidRequest()
    if not isinstance(product['categoria_id'], int):
        invalid_req.add_error('value', 'product id must be integer')

    if invalid_req.has_errors():
        return invalid_req

    return ValidRequest(data=product)
