# pylint: disable=c0116
from unittest import mock

import pytest

from src.requests.category_update import build_update_category_request
from src.use_cases.category_update import category_update_use_case


@pytest.fixture
def category_to_update():
    return {
        'id': 1,
        'ativo': False,
    }


def test_update_client_success(category_to_update):
    repo = mock.Mock()

    repo.update_category.return_value = category_to_update

    request = build_update_category_request(category_to_update)

    response = category_update_use_case(repo, request)

    repo.update_category.assert_called_with(category_to_update)
    assert response.value == category_to_update
