"""Test module for transaction postgres repository"""
# pylint: disable=c0116
# pylint: disable=w0613
import pytest
from sqlalchemy.exc import IntegrityError

from src.repository.postgres.postgresrepo_transaction import (
    PostgresRepoTransaction,
)

# The module attribute pytestmark labels every test in the module with the tag integration
pytestmark = pytest.mark.integration


def test_transaction_repository_list_without_parameters(
    app_configuration, pg_session
):
    repo = PostgresRepoTransaction(app_configuration)

    transactions = repo.list_transaction()

    assert len(transactions) == 4


def test_transaction_repository_list_with_code_equal_filter(
    app_configuration, pg_session
):
    repo = PostgresRepoTransaction(app_configuration)

    transaction = repo.list_transaction(filters={'id__eq': 1})

    assert len(transaction) == 1
    assert transaction[0].ativo is True


def test_transaction_repository_list_with_ativo_false_filter(
    app_configuration, pg_session
):
    repo = PostgresRepoTransaction(app_configuration)

    transaction_inactive = repo.list_transaction(filters={'ativo__eq': False})

    assert len(transaction_inactive) == 2


def test_transaction_repository_list_with_produto_id_equal_filter(
    app_configuration, pg_session
):
    repo = PostgresRepoTransaction(app_configuration)

    transaction = repo.list_transaction(filters={'produto_id__eq': 1})

    assert len(transaction) == 4


def test_transaction_repository_list_with_client_id_equal_filter(
    app_configuration, pg_session
):
    repo = PostgresRepoTransaction(app_configuration)

    transaction = repo.list_transaction(filters={'client_id__eq': 1})

    assert len(transaction) == 1


def test_transaction_repository_create_from_dictionary(
    app_configuration, pg_session
):
    repo = PostgresRepoTransaction(app_configuration)

    transaction_dict = {
        'client_id': 1,
        'transactions': [
            {
                'code': 'abcec028-8e61-4504-a0f3-772f08d11d70',
                'date': '2023-11-30 12:30:00',
                'transacao_items': [
                    {'sku': 'ABC123', 'quantidade': 2},
                    {'sku': 'XYZ456', 'quantidade': 1},
                    {'sku': '123DEF', 'quantidade': 3},
                ],
            },
            {
                'code': '1c466ee0-7555-4272-b58a-574f4782d30c',
                'date': '2023-11-29 15:45:00',
                'transacao_items': [
                    {'sku': 'LMN789', 'quantidade': 1},
                    {'sku': '456GHI', 'quantidade': 5},
                ],
            },
            {
                'code': '2c832006-729c-4389-b8dc-67bf0948811f',
                'date': '2023-11-28 09:00:00',
                'transacao_items': [
                    {'sku': 'JKL321', 'quantidade': 2},
                    {'sku': '789MNO', 'quantidade': 4},
                ],
            },
        ],
    }

    repo.create_transaction(transaction_dict)

    assert True


def test_transaction_repository_create_error(app_configuration):
    repo = PostgresRepoTransaction(app_configuration)

    transaction_dict = {}

    with pytest.raises(IntegrityError):
        repo.create_transaction(transaction_dict)
