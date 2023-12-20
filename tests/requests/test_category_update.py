from datetime import datetime

from src.requests.category_update import build_update_category_request


def test_build_category_update_request():
    category_to_update = {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'descricao': 'Categoria A',
        'ativo': True,
    }
    request = build_update_category_request(category_to_update)

    assert bool(request) is True
    assert 'dt_alteracao' in category_to_update
    assert isinstance(category_to_update['dt_alteracao'], datetime)
