"""Test module for Category serializer"""
import json
from datetime import datetime

from freezegun import freeze_time

from src.domain.transaction import Transaction
from src.serializers.transaction import TransactionJsonEncoder


@freeze_time('2023-01-01 00:00:00')
def test_serialize_domain_transaction():
    transaction = Transaction(
        id=1,
        code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
        client_id=1,
        produto_id=1,
        quantidade=10,
        dt_inclusao=datetime.now(),
        dt_transacao=datetime(2023, 10, 10, 10, 0, 0),
        dt_alteracao=None,
        ativo=True,
    )

    expected_json = """
        {
            "id": 1,
            "code": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
            "client_id": 1,
            "produto_id": 1,
            "quantidade": 10,
            "dt_inclusao": "2023-01-01 00:00:00",
            "dt_transacao": "2023-10-10 10:00:00",
            "dt_alteracao": null,
            "ativo": true
        }
        """
    json_transaction = json.dumps(transaction, cls=TransactionJsonEncoder)

    assert json.loads(json_transaction) == json.loads(expected_json)
