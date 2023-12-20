"""Test module for the Produtc entity"""
# pylint: disable=c0116
from src.domain.product import Product


def test_product_model_init():
    product = Product(
        nome='My product',
        descricao='My description',
        sku='0123456789',
        categoria_id=1,
    )

    assert product.id is None
    assert product.code is None
    assert product.nome == 'My product'
    assert product.descricao == 'My description'
    assert product.sku == '0123456789'
    assert product.categoria_id == 1


def test_product_model_init_with_defaults():
    product = Product(
        id=1,
        code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
        nome='My product',
        descricao='My description',
        sku='0123456789',
        categoria_id=1,
        dt_inclusao='01/01/2023, 00:00:00',
        dt_alteracao='01/01/2023, 00:00:00',
        ativo=True,
    )

    assert product.id == 1
    assert product.code == 'f853578c-fc0f-4e65-81b8-566c5dffa35a'
    assert product.nome == 'My product'
    assert product.descricao == 'My description'
    assert product.sku == '0123456789'
    assert product.categoria_id == 1
    assert product.dt_inclusao == '01/01/2023, 00:00:00'
    assert product.dt_alteracao == '01/01/2023, 00:00:00'
    assert product.ativo is True


def test_product_model_from_dict():
    init_dict = {
        'nome': 'My product',
        'descricao': 'My description',
        'sku': '0123456789',
        'categoria_id': 1,
    }

    product = Product.from_dict(init_dict)

    assert product.id is None
    assert product.code is None
    assert product.nome == 'My product'
    assert product.descricao == 'My description'
    assert product.sku == '0123456789'
    assert product.categoria_id == 1


def test_product_model_to_dict():
    init_dict = {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'nome': 'My product',
        'descricao': 'My description',
        'sku': '0123456789',
        'categoria_id': 1,
        'dt_inclusao': '01/01/2023, 00:00:00',
        'dt_alteracao': '01/01/2023, 00:00:00',
        'ativo': True,
    }

    product = Product.from_dict(init_dict)

    assert product.to_dict() == init_dict
