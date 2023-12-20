"""Test module for create category"""
# pylint: disable=c0116
from unittest import mock

import pytest

from src.requests.category_create import build_create_category_request
from src.responses import ResponseTypes
from src.use_cases.category_create import category_create_use_case


@pytest.fixture
def category_dict():
    return {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'descricao': 'description text',
        'dt_inclusao': '01/01/2023 00:00:00',
        'dt_alteracao': None,
        'ativo': True,
        'client_id': 1,
    }


def test_create_category(category_dict):
    repo = mock.Mock()

    new_category = {
        'descricao': 'description text',
        'client_id': 1,
    }

    repo.list_category.return_value = []
    repo.create_category.return_value = category_dict

    request = build_create_category_request(new_category)

    result = category_create_use_case(repo, request)

    assert bool(result) is True
    repo.create_category.assert_called_with(new_category)
    assert result.value == category_dict


def test_create_category_already_exists(category_dict):
    repo = mock.Mock()
    repo.list_category.return_value = category_dict

    request = build_create_category_request(category_dict)

    result = category_create_use_case(repo, request)

    assert bool(result) is False
    repo.list_category.assert_called_with(
        filters={
            'client_id': request.data['client_id'],
            'descricao__eq': request.data['descricao'],
        }
    )
    assert result.value == {
        'type': ResponseTypes.DOMAIN_ERROR,
        'message': 'Categoria já cadastrada',
    }


def test_create_category_without_cliend_id():
    repo = mock.Mock()

    new_category = {
        'descricao': 'description text',
        'client_id': '',
    }

    request = build_create_category_request(new_category)

    result = category_create_use_case(repo, request)

    assert bool(result) is False
    assert result.value == {
        'type': ResponseTypes.PARAMETERS_ERROR,
        'message': 'value: client id must be an integer',
    }
