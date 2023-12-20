from src.requests.transaction_create import build_transaction_create_request


def test_build_transaction_create_request():
    transaction = {'client_id': 1, 'produto_id': 1, 'quantidade': 10}

    request = build_transaction_create_request(transaction)

    assert bool(request) is True
