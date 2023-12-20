"""Test module for transaction list use cases"""
# pylint: disable=w0621
from unittest import mock

import pytest

from src.domain.transaction import Transaction
from src.requests.transaction_list import build_transaction_list_request
from src.responses import ResponseTypes
from src.use_cases.transaction_list import transaction_list_use_case


@pytest.fixture
def domain_transaction():
    transaction_1 = Transaction(
        id=1,
        code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
        client_id=1,
        produto_id=1,
        quantidade=10,
        dt_inclusao='01/01/2023 00:00:00',
        dt_transacao='2023-01-01 00:00:00.000',
        dt_alteracao=None,
        ativo=True,
    )
    transaction_2 = Transaction(
        id=2,
        code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
        client_id=1,
        produto_id=1,
        quantidade=10,
        dt_inclusao='01/01/2023 00:00:00',
        dt_transacao='2023-01-01 00:00:00.000',
        dt_alteracao=None,
        ativo=True,
    )
    transaction_3 = Transaction(
        id=3,
        code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
        client_id=1,
        produto_id=1,
        quantidade=10,
        dt_inclusao='01/01/2023 00:00:00',
        dt_transacao='2023-01-01 00:00:00.000',
        dt_alteracao=None,
        ativo=True,
    )
    transaction_4 = Transaction(
        id=4,
        code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
        client_id=1,
        produto_id=1,
        quantidade=10,
        dt_inclusao='01/01/2023 00:00:00',
        dt_transacao='2023-01-01 00:00:00.000',
        dt_alteracao=None,
        ativo=True,
    )

    return [transaction_1, transaction_2, transaction_3, transaction_4]


def test_transaction_list_without_parameters(domain_transaction):
    repo = mock.Mock()
    repo.list_transaction.return_value = domain_transaction

    request = build_transaction_list_request()

    response = transaction_list_use_case(repo, request)

    assert bool(response) is True
    repo.list_transaction.assert_called_with(filters=None)
    assert response.value == domain_transaction


def test_transaction_list_with_id_equal_filters(domain_transaction):
    repo = mock.Mock()
    repo.list_transaction.return_value = domain_transaction

    qry_filters = {'id__eq': 1}
    request = build_transaction_list_request(filters=qry_filters)

    response = transaction_list_use_case(repo, request)

    assert bool(response) is True
    repo.list_transaction.assert_called_with(filters=qry_filters)
    assert response.value == domain_transaction


def test_transaction_list_handles_generic_error():
    repo = mock.Mock()
    repo.list_transaction.side_effect = Exception('Just an error message')

    request = build_transaction_list_request(filters={})

    response = transaction_list_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseTypes.SYSTEM_ERROR,
        'message': 'Exception: Just an error message',
    }


def test_transaction_list_handles_bad_request():
    repo = mock.Mock()

    request = build_transaction_list_request(filters=5)

    response = transaction_list_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseTypes.PARAMETERS_ERROR,
        'message': 'filters: Is not iterable',
    }
