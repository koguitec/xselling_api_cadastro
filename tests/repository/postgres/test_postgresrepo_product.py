"""Test module for product postgres repository"""
# pylint: disable=c0116
# pylint: disable=w0613
import pytest
from sqlalchemy.exc import IntegrityError

from src.repository.postgres.postgresrepo_product import PostgresRepoProduct

# The module attribute pytestmark labels every test in the module with the tag integration
pytestmark = pytest.mark.integration


def test_product_repository_create_from_dictionary(
    app_configuration, pg_session
):
    repo = PostgresRepoProduct(app_configuration)

    product_dict = {
        'nome': 'My new product',
        'descricao': 'My new description',
        'sku': '0101010101',
        'categoria_id': 1,
    }

    product = repo.create_product(product_dict)

    assert product.id == 5
    assert product.nome == 'My new product'
    assert product.descricao == 'My new description'
    assert product.sku == '0101010101'
    assert product.categoria_id == 1


def test_product_repository_list_without_parameters(
    app_configuration, pg_session
):
    repo = PostgresRepoProduct(app_configuration)

    products = repo.list_product()

    assert len(products) == 5


def test_product_repository_update(app_configuration, pg_session):
    repo = PostgresRepoProduct(app_configuration)

    product_data_to_update = {'id': 1, 'ativo': False}

    product = repo.update_product(product_data_to_update)

    assert product.ativo is False


def test_product_epository_create_error(app_configuration, pg_session):
    repo = PostgresRepoProduct(app_configuration)

    product_dict = {}

    with pytest.raises(IntegrityError):
        repo.create_product(product_dict)


def test_product_repository_update_without_id_error(
    app_configuration, pg_session
):
    repo = PostgresRepoProduct(app_configuration)

    product_dict = {}

    with pytest.raises(KeyError):
        repo.update_product(product_dict)
