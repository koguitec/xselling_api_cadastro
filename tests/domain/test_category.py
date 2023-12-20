"""Test module for the category entity"""
# pylint: disable=c0116
from src.domain.category import Category


def test_client_model_init():
    category = Category(
        descricao='description text',
        client_id=1,
    )

    assert category.id is None
    assert category.code is None
    assert category.descricao == 'description text'
    assert category.dt_inclusao is None
    assert category.dt_alteracao is None
    assert category.ativo is True
    assert category.client_id == 1


def test_category_model_from_dict():
    init_dict = {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'descricao': 'description text',
        'dt_inclusao': '01/01/2023 00:00:00',
        'dt_alteracao': None,
        'ativo': True,
        'client_id': 1,
    }

    category = Category.from_dict(init_dict)

    assert category.id == 1
    assert category.code == 'f853578c-fc0f-4e65-81b8-566c5dffa35a'
    assert category.descricao == 'description text'
    assert category.dt_inclusao == '01/01/2023 00:00:00'
    assert category.dt_alteracao is None
    assert category.ativo is True
    assert category.client_id == 1


def test_category_model_to_dict():
    init_dict = {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'descricao': 'description text',
        'dt_inclusao': '01/01/2023 00:00:00',
        'dt_alteracao': None,
        'ativo': True,
        'client_id': 1,
    }

    category = Category.from_dict(init_dict)

    assert category.to_dict() == init_dict


def test_category_model_comparison():
    init_dict = {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'descricao': 'description text',
        'dt_inclusao': '01/01/2023 00:00:00',
        'dt_alteracao': None,
        'ativo': True,
        'client_id': 1,
    }

    category1 = Category.from_dict(init_dict)
    category2 = Category.from_dict(init_dict)

    assert category1 == category2
