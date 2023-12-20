"""Test module for client postgres repository"""
# pylint: disable=c0116
# pylint: disable=w0613
import uuid
from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from src.domain.auth_jwt import AuthJwt, TokenTypeEnum
from src.repository.postgres.postgresrepo_client import PostgresRepoClient

# The module attribute pytestmark labels every test in the module with the tag integration
pytestmark = pytest.mark.integration


def test_client_repository_list_without_parameters(
    app_configuration, pg_session, pg_client_test_data
):
    repo = PostgresRepoClient(app_configuration)

    clients = repo.list_client()

    assert len(clients) == 4


def test_client_repository_list_with_id_equal_filter(
    app_configuration, pg_session, pg_client_test_data
):
    repo = PostgresRepoClient(app_configuration)

    client = repo.list_client(filters={'id__eq': 1})

    assert client[0].id == 1


def test_client_repository_list_with_code_equal_filter(
    app_configuration, pg_session, pg_client_test_data
):
    repo = PostgresRepoClient(app_configuration)

    client = repo.list_client(
        filters={'code__eq': uuid.UUID('f853578c-fc0f-4e65-81b8-566c5dffa35a')}
    )

    assert client[0].id == 1
    assert client[0].code == uuid.UUID('f853578c-fc0f-4e65-81b8-566c5dffa35a')
    assert isinstance(client[0].dt_inclusao, datetime)


def test_client_repository_list_with_cnpj_equal_filter(
    app_configuration, pg_session
):
    repo = PostgresRepoClient(app_configuration)

    client = repo.list_client(filters={'cnpj__eq': '00.000.000/0000-01'})

    assert len(client) == 1
    assert client[0].id == 1
    assert client[0].cnpj == '00.000.000/0000-01'


def test_client_repository_list_with_ativo_false_filter(
    app_configuration, pg_session, pg_client_test_data
):
    repo = PostgresRepoClient(app_configuration)

    clients_inactive = repo.list_client(filters={'ativo__eq': False})

    assert len(clients_inactive) == 0


def test_client_repository_create_from_dictionary(
    app_configuration, pg_session
):
    repo = PostgresRepoClient(app_configuration)

    client_dict = {
        'cnpj': '00.000.000/0000-10',
        'email': 'my_new_email@email.com',
        'razao_social': 'My new company',
    }

    client = repo.create_client(client_dict)

    assert client.id == 5
    assert client.cnpj == '00.000.000/0000-10'
    assert client.email == 'my_new_email@email.com'
    assert client.razao_social == 'My new company'


def test_client_repository_update(
    app_configuration, pg_session, pg_client_test_data
):
    repo = PostgresRepoClient(app_configuration)

    client_data_to_update = {
        'id': 1,
        'ativo': False,
    }
    repo.update_client(client_data_to_update)

    updated_client = repo.list_client(filters={'id__eq': 1})

    assert updated_client[0].ativo is False
    assert updated_client[0].code == uuid.UUID(
        'f853578c-fc0f-4e65-81b8-566c5dffa35a'
    )


def test_client_repository_create_error(app_configuration, pg_session):
    repo = PostgresRepoClient(app_configuration)

    new_client = {}

    with pytest.raises(IntegrityError):
        repo.create_client(new_client)


def test_client_repository_update_without_id_error(
    app_configuration, pg_session
):
    repo = PostgresRepoClient(app_configuration)

    new_client = {}

    with pytest.raises(KeyError):
        repo.update_client(new_client)


def test_token_repository_create_from_dictionary(
    app_configuration, pg_session
):
    repo = PostgresRepoClient(app_configuration)

    token_dict = {
        'jti': 'a;dfsjklhgvna;dfjkbalkdfjbvakdfnvaoakl;dfsjnvanvdf;kl',
        'client_id': 3,
        'token_type': TokenTypeEnum.REFRESH.value,
        'revoked': False,
        'expires': datetime.now(),
    }

    token = repo.create_token(token_dict)

    assert token.id == 1
    assert token.client_id == 3
    assert token.revoked is False
    assert isinstance(token, AuthJwt)
    assert isinstance(token.jti, str)
    assert isinstance(token.expires, datetime)


def test_token_repository_create_error(app_configuration, pg_session):
    repo = PostgresRepoClient(app_configuration)

    token_dict = {}

    with pytest.raises(IntegrityError):
        repo.create_token(token_dict)
