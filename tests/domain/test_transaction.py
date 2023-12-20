"""Test module for the transaction entity"""
# pylint: disable=c0116
from datetime import datetime

from freezegun import freeze_time

from src.domain.transaction import Transaction


@freeze_time('2023-01-01 00:00:00')
def test_transaction_model_init():
    transaction = Transaction(
        client_id=1, produto_id=1, quantidade=10, dt_transacao=datetime.now()
    )

    assert transaction.id is None
    assert transaction.code is None
    assert transaction.client_id == 1
    assert transaction.produto_id == 1
    assert transaction.quantidade == 10
    assert transaction.dt_transacao == datetime(2023, 1, 1, 00, 00, 00)
    assert transaction.dt_inclusao is None
    assert transaction.dt_alteracao is None


@freeze_time('2023-01-01 00:00:00')
def test_transaction_model_from_dict():
    init_dict = {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'client_id': 1,
        'produto_id': 1,
        'quantidade': 10,
        'dt_inclusao': datetime.now(),
        'dt_transacao': datetime(2023, 10, 10, 10, 00, 00),
        'dt_alteracao': None,
        'ativo': True,
    }

    transaction = Transaction.from_dict(init_dict)

    assert transaction.id == 1
    assert transaction.code == 'f853578c-fc0f-4e65-81b8-566c5dffa35a'
    assert transaction.client_id == 1
    assert transaction.produto_id == 1
    assert transaction.quantidade == 10
    assert transaction.dt_inclusao == datetime(2023, 1, 1, 00, 00, 00)
    assert transaction.dt_transacao == datetime(2023, 10, 10, 10, 00, 00)
    assert transaction.dt_alteracao is None
    assert transaction.ativo is True


@freeze_time('2023-01-01 00:00:00')
def test_transaction_model_to_dict():
    init_dict = {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'client_id': 1,
        'produto_id': 1,
        'quantidade': 10,
        'dt_inclusao': datetime.now(),
        'dt_transacao': datetime(2023, 10, 10, 10, 00, 00),
        'dt_alteracao': None,
        'ativo': True,
    }

    transaction = Transaction.from_dict(init_dict)

    assert transaction.to_dict() == init_dict


@freeze_time('2023-01-01 00:00:00')
def test_transaction_model_comparison():
    init_dict = {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'client_id': 1,
        'produto_id': 1,
        'quantidade': 10,
        'dt_inclusao': datetime.now(),
        'dt_transacao': datetime(2023, 10, 10, 10, 00, 00),
        'dt_alteracao': None,
        'ativo': True,
    }

    transaction1 = Transaction.from_dict(init_dict)
    transaction2 = Transaction.from_dict(init_dict)

    assert transaction1 == transaction2
