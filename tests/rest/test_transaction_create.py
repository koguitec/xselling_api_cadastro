import json
from unittest import mock

from src.responses import ResponseSuccess

transaction_dict = {'client_id': 1, 'produto_id': 1, 'quantidade': 10}


@mock.patch('application.rest.transaction.transaction_create_use_case')
def test_post(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(transaction_dict)

    http_response = client.post('/transactions', json=transaction_dict)

    assert json.loads(http_response.data.decode('utf-8')) == transaction_dict

    mock_use_case.assert_called()

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.transaction.transaction_create_use_case')
def test_post_with_missing_data(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(transaction_dict)

    transaction_dict.pop('quantidade')
    transaction_dict_missing_data = transaction_dict

    http_response = client.post(
        '/transactions', json=transaction_dict_missing_data
    )

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.transaction.transaction_create_use_case')
def test_post_with_extra_data(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(transaction_dict)

    transaction_dict.update({'extra': 'field'})
    transaction_dict_missing_data = transaction_dict

    http_response = client.post(
        '/transactions', json=transaction_dict_missing_data
    )

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'
