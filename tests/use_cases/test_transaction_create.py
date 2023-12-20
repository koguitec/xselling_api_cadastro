from unittest import mock

import pytest

from src.requests.transaction_create import build_transaction_create_request
from src.use_cases.transaction_create import transaction_create_use_case


@pytest.fixture
def transaction_dict():
    return {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'client_id': 1,
        'produto_id': 1,
        'quantidade': 10,
        'dt_inclusao': '01/01/2023 00:00:00',
        'dt_alteracao': None,
        'ativo': True,
    }


def test_transaction_create(transaction_dict):
    repo = mock.Mock()
    repo.create_transaction.return_value = transaction_dict

    new_transaction = {'client_id': 1, 'categoria_id': 1, 'quantidade': 10}

    request = build_transaction_create_request(new_transaction)

    result = transaction_create_use_case(repo, request)

    assert bool(result) is True
    repo.create_transaction.assert_called_with(new_transaction)
    assert result.value == transaction_dict
