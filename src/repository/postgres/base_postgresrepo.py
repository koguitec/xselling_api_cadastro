"""Base class for PostgresRepo"""
import os

from sqlmodel import Session, SQLModel, create_engine


class BasePostgresRepo:
    """Postgres repository"""

    def __init__(self):
        self._connection_string = 'mssql+pyodbc://{}:{}@{}/{}?TrustServerCertificate=yes&driver=ODBC+Driver+18+for+SQL+Server'.format(
            os.environ['MSSQL_USER'],
            os.environ['MSSQL_SA_PASSWORD'],
            os.environ['MSSQL_HOSTNAME'],
            os.environ['APPLICATION_DB'],
        )

        self.engine = create_engine(self._connection_string)
        SQLModel.metadata.create_all(self.engine)
        SQLModel.metadata.bind = self.engine

    def _create_session(self, *, expire_on_commit=True):
        return Session(bind=self.engine, expire_on_commit=expire_on_commit)
