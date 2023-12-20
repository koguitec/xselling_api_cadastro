# pylint: disable=c0116
import json
from unittest import mock

import pytest

from src.responses import ResponseSuccess


@pytest.fixture
def category_dict():
    return {
        'id': 1,
        'descricao': 'description text',
        'ativo': True,
    }


@mock.patch('application.rest.category.category_update_use_case')
def test_put(mock_use_case, client, category_dict):
    mock_use_case.return_value = ResponseSuccess(category_dict)

    http_response = client.put('/categories', json=category_dict)

    assert json.loads(http_response.data.decode('utf-8')) == category_dict

    mock_use_case.assert_called()

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.category.category_update_use_case')
def test_put_without_body(mock_use_case, client, category_dict):
    mock_use_case.return_value = ResponseSuccess(category_dict)

    http_response = client.put('/categories', json={})

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.category.category_update_use_case')
def test_put_with_missing_data(mock_use_case, client, category_dict):
    mock_use_case.return_value = ResponseSuccess(category_dict)

    category_dict.pop('id')
    category_dict_missing_data = category_dict

    http_response = client.put('/categories', json=category_dict_missing_data)

    # assert "error" in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.category.category_update_use_case')
def test_put_with_extra_data(mock_use_case, client, category_dict):
    mock_use_case.return_value = ResponseSuccess(category_dict)

    category_dict.update({'extra': 'field'})
    category_dict_extra_data = category_dict

    http_response = client.put('/categories', json=category_dict_extra_data)

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'
