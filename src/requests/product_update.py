from datetime import datetime
from typing import Dict

from src.requests.validation.invalid_request import InvalidRequest
from src.requests.validation.valid_request import ValidRequest


def build_update_product_request(product: Dict):
    """Factory for requests

    Args:
        client (dict): Dictionary containing client data

    Returns:
        Object: Return InvalidRequest if errors, otherwise, returns
        ValidRequest,
    """
    invalid_req = InvalidRequest()

    if 'id' not in product and 'code' not in product:
        invalid_req.add_error('value', 'Must contain id or code to update')

    if invalid_req.has_errors():
        return invalid_req

    product.update({'dt_alteracao': datetime.now()})
    return ValidRequest(data=product)
