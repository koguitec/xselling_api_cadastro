"""Test module for client list use case"""
# pylint: disable=w0621
# pylint: disable=c0116
import pytest

from src.domain.category import Category
from src.repository.in_memory.memrepo_category import MemRepoCategory


@pytest.fixture
def category_dicts():
    return [
        {
            'descricao': 'categoria A',
            'dt_inclusao': '18/11/2023, 14:44:12',
            'dt_alteracao': None,
            'ativo': True,
            'client_id': [1],
        },
        {
            'descricao': 'categoria B',
            'dt_inclusao': '18/11/2023, 14:44:12',
            'dt_alteracao': None,
            'ativo': True,
            'client_id': [1],
        },
        {
            'descricao': 'categoria C',
            'dt_inclusao': '18/11/2023, 14:44:12',
            'dt_alteracao': None,
            'ativo': False,
            'client_id': [2],
        },
        {
            'descricao': 'categoria D',
            'dt_inclusao': '18/11/2023, 14:44:12',
            'dt_alteracao': None,
            'ativo': False,
            'client_id': [2],
        },
    ]


def test_repository_create_category(category_dicts):
    repo = MemRepoCategory(category_dicts)

    new_category = {
        'descricao': 'description text',
        'dt_inclusao': '18/11/2023, 14:44:12',
        'dt_alteracao': None,
        'ativo': True,
        'client_id': [1],
    }

    repo.create_category(new_category)

    assert len(category_dicts) == 5


def test_repository_list_category_without_params(category_dicts):
    repo = MemRepoCategory(category_dicts)

    result = [Category.from_dict(c) for c in category_dicts]

    assert repo.list_category() == result


def test_repository_list_with_ativo_equal_filter(category_dicts):
    repo = MemRepoCategory(category_dicts)

    categories = repo.list_category({'ativo__eq': True})

    assert len(categories) == 2


def test_repository_list_with_id_equal_true_filter(category_dicts):
    repo = MemRepoCategory(category_dicts)

    categories = repo.list_category({'ativo__eq': True})

    assert len(categories) == 2


def test_repository_update_client(category_dicts):
    repo = MemRepoCategory(category_dicts)

    new_category_data = {
        'descricao': 'categoria D',
        'dt_inclusao': '18/11/2023, 14:44:12',
        'dt_alteracao': None,
        'ativo': True,
        'client_id': [2],
    }

    repo.update_category(new_category_data)

    updated_client = {}
    for client in category_dicts:
        if client['descricao'] == 'categoria D':
            updated_client = client

    assert len(category_dicts) == 4
    assert updated_client['ativo'] is True
