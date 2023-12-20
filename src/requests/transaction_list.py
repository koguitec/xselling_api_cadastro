from collections.abc import Mapping

from src.requests.validation.invalid_request import InvalidRequest
from src.requests.validation.valid_request import ValidRequest


def build_transaction_list_request(filters=None):
    """Factory for requests

    Args:
        filters (Dict, optional): Dictionary containing parameter filter and
        value. Defaults to None.

    Returns:
        Object: Return InvalidRequest if errors, otherwise, returns
        ValidRequest,
    """
    accepted_filters = [
        'id__eq',
        'code__eq',
        'ativo__eq',
        'produto_id__eq',
        'client_id__eq',
    ]
    invalid_req = InvalidRequest()

    if filters is not None:
        if not isinstance(filters, Mapping):
            invalid_req.add_error('filters', 'Is not iterable')
            return invalid_req

        for key, value in filters.items():
            if key not in accepted_filters:
                invalid_req.add_error('filters', f'Key {key} cannot be used')

        if invalid_req.has_errors():
            return invalid_req

    return ValidRequest(filters=filters)
