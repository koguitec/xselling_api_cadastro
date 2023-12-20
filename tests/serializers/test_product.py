"""Test module for Category serializer"""
import json

from src.domain.product import Product
from src.serializers.product import ProductJsonEncoder


def test_serialize_domain_product():
    product = Product(
        id=1,
        code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
        nome='My product',
        descricao='My description',
        sku='0123456789',
        categoria_id=1,
        dt_inclusao='01/01/2023 00:00:00',
        dt_alteracao=None,
        ativo=True,
    )

    excepted_json = """
        {
            "id": 1,
            "code": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
            "nome": "My product",
            "descricao": "My description",
            "sku": "0123456789",
            "categoria_id": 1,
            "dt_inclusao": "01/01/2023 00:00:00",
            "dt_alteracao": null,
            "ativo": true
        }
        """

    json_product = json.dumps(product, cls=ProductJsonEncoder)

    assert json.loads(json_product) == json.loads(excepted_json)
