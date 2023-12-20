"""Configuratin module for integration testing for Postgres
The fixtures contains code that is specific to Postgres, so it is better to
keep the code separated in a more specific file conftest.py
"""

import os
import uuid
from datetime import datetime

# pylint: disable=w0621
# pylint: disable=c0116
# pylint: disable=c0103
# pylint: disable=c0209
import pytest
import sqlmodel

from src.repository.postgres.postgres_objects import AuthJwt as PgAuthToken
from src.repository.postgres.postgres_objects import Category as PgCategory
from src.repository.postgres.postgres_objects import Client as PgClient
from src.repository.postgres.postgres_objects import Product as PgProduct
from src.repository.postgres.postgres_objects import (
    Transaction as PgTransaction,
)


@pytest.fixture(scope='session')
def pg_session_empty(app_configuration):
    conn_str = 'mssql+pyodbc://{}:{}@{}/{}?TrustServerCertificate=yes&driver=ODBC+Driver+18+for+SQL+Server'.format(
        os.environ['MSSQL_USER'],
        os.environ['MSSQL_SA_PASSWORD'],
        os.environ['MSSQL_HOSTNAME'],
        os.environ['APPLICATION_DB'],
    )

    engine = sqlmodel.create_engine(conn_str)
    connection = engine.connect()

    sqlmodel.SQLModel.metadata.create_all(engine)
    sqlmodel.SQLModel.metadata.bind = engine

    DBSession = sqlmodel.Session(bind=engine)
    session = DBSession

    yield session

    session.close()
    connection.close()


@pytest.fixture(scope='session')
def pg_client_test_data():
    return [
        {
            'code': uuid.UUID('f853578c-fc0f-4e65-81b8-566c5dffa35a'),
            'razao_social': 'My company 1',
            'cnpj': '00.000.000/0000-01',
            'email': 'mycompany_1@email.com',
            'dt_inclusao': datetime.now(),
            'dt_alteracao': datetime.now(),
        },
        {
            'razao_social': 'My company 2',
            'cnpj': '00.000.000/0000-02',
            'email': 'mycompany_2@email.com',
            'dt_inclusao': datetime.now(),
            'dt_alteracao': None,
        },
        {
            'razao_social': 'My company 3',
            'cnpj': '00.000.000/0000-03',
            'email': 'mycompany_3@email.com',
            'dt_inclusao': datetime.now(),
            'dt_alteracao': None,
        },
        {
            'razao_social': 'My company 4',
            'cnpj': '00.000.000/0000-04',
            'email': 'mycompany_4@email.com',
            'dt_inclusao': datetime.now(),
            'dt_alteracao': None,
        },
    ]


@pytest.fixture(scope='session')
def pg_category_test_data():
    return [
        {'descricao': 'categoria A', 'client_id': 1, 'ativo': True},
        {'descricao': 'categoria B', 'client_id': 1, 'ativo': True},
        {'descricao': 'categoria C', 'client_id': 2, 'ativo': False},
        {'descricao': 'categoria D', 'client_id': 2, 'ativo': False},
    ]


@pytest.fixture(scope='session')
def pg_product_test_data():
    return [
        {
            'nome': 'Produto A',
            'descricao': 'descricao A',
            'sku': '0123456789',
            'categoria_id': 1,
            'ativo': True,
        },
        {
            'nome': 'Produto B',
            'descricao': 'descricao B',
            'sku': '0123456789',
            'categoria_id': 1,
            'ativo': True,
        },
        {
            'nome': 'Produto C',
            'descricao': 'descricao C',
            'sku': '0123456789',
            'categoria_id': 2,
            'ativo': False,
        },
        {
            'nome': 'Produto D',
            'descricao': 'descricao D',
            'sku': '0123456789',
            'categoria_id': 2,
            'ativo': False,
        },
    ]


@pytest.fixture(scope='session')
def pg_transaction_test_data():
    return [
        {
            'client_id': 1,
            'produto_id': 1,
            'quantidade': 5,
            'ativo': True,
        },
        {
            'client_id': 2,
            'produto_id': 1,
            'quantidade': 5,
            'ativo': True,
        },
        {
            'client_id': 3,
            'produto_id': 1,
            'quantidade': 5,
            'ativo': False,
        },
        {
            'client_id': 4,
            'produto_id': 1,
            'quantidade': 5,
            'ativo': False,
        },
    ]


@pytest.fixture(scope='package')
def pg_session(
    pg_session_empty,
    pg_client_test_data,
    pg_category_test_data,
    pg_product_test_data,
    pg_transaction_test_data,
):
    """Fills the database with Postgress objects created with the test data for
    every test that is run. These are not entities, but Postgress objects we
    create to map them.
    """
    for idx, client in enumerate(pg_client_test_data):
        ### CREATE CLIENTS ###
        new_client = PgClient(**client)
        pg_session_empty.add(new_client)
        pg_session_empty.commit()

        ### CREATE CATEGORIES ###
        # Assuming pg_category_test_data has the same length as pg_client_test_data
        category_data = pg_category_test_data[idx]
        # Assuming the FK relationship between client and category
        category_data.update({'client_id': new_client.id})
        new_category = PgCategory(**category_data)

        pg_session_empty.add(new_category)
        pg_session_empty.commit()

        ### CREATE PRODUCTS ###
        # Assuming the same length of category and product arrays
        product_data = pg_product_test_data[idx]
        # Assuming the FK relationship between category and product
        product_data.update({'categoria_id': new_category.id})
        new_product = PgProduct(**product_data)

        pg_session_empty.add(new_product)
        pg_session_empty.commit()

        ### CREATE TRANSACTIONS ###
        # Assuming the same length of product and transaction arrays
        transaction_data = pg_transaction_test_data[idx]
        new_transaction = PgTransaction(**transaction_data)

        pg_session_empty.add(new_transaction)
        pg_session_empty.commit()

    yield pg_session_empty

    # Clean up after test
    pg_session_empty.query(PgAuthToken).delete()
    pg_session_empty.query(PgTransaction).delete()
    pg_session_empty.query(PgProduct).delete()
    pg_session_empty.query(PgCategory).delete()
    pg_session_empty.query(PgClient).delete()
