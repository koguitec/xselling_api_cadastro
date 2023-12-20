"""Test module for Category serializer"""
import json

from src.domain.category import Category
from src.serializers.category import CategoryJsonEncoder


def test_serialize_domain_category():
    category = Category(
        id=1,
        code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
        descricao='description text',
        dt_inclusao='01/01/2023 00:00:00',
        client_id=1,
        dt_alteracao=None,
        ativo=True,
    )

    excepted_json = """
        {
            "id": 1,
            "code": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
            "descricao": "description text",
            "client_id": 1,
            "dt_inclusao": "01/01/2023 00:00:00",
            "dt_alteracao": null,
            "ativo": true
        }
        """

    json_category = json.dumps(category, cls=CategoryJsonEncoder)

    assert json.loads(json_category) == json.loads(excepted_json)
