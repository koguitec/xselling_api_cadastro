"""Test module for Client serializer"""
import json

from src.domain.client import Client
from src.serializers.client import ClientJsonEncoder


def test_serialize_domain_client():
    client = Client(
        id=1,
        code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
        razao_social='My company',
        cnpj='00.000.000/0000-00',
        email='mycompany@email.com',
        dt_inclusao='01/01/2023 00:00:00',
        dt_alteracao=None,
        ativo=True,
    )

    excepted_json = """
        {
            "id": 1,
            "code": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
            "razao_social": "My company",
            "cnpj": "00.000.000/0000-00",
            "email": "mycompany@email.com",
            "dt_inclusao": "01/01/2023 00:00:00",
            "dt_alteracao": null,
            "ativo": true
        }
        """

    json_client = json.dumps(client, cls=ClientJsonEncoder)

    assert json.loads(json_client) == json.loads(excepted_json)
