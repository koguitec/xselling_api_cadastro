"""Module for the Postgres database"""
import uuid
from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


def generate_uuid_str() -> str:
    return str(uuid.uuid4())


class Client(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(default_factory=generate_uuid_str, nullable=False)
    razao_social: str
    cnpj: str
    email: str
    dt_inclusao: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    dt_alteracao: datetime | None = None
    ativo: bool = True


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(default_factory=generate_uuid_str, nullable=False)
    descricao: str
    dt_inclusao: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    dt_alteracao: datetime | None = None
    ativo: bool = True

    client_id: int | None = Field(foreign_key='client.id')


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(default_factory=generate_uuid_str, nullable=False)
    nome: str
    descricao: str
    sku: str
    dt_inclusao: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    dt_alteracao: datetime | None = None
    ativo: bool = True

    categoria_id: int | None = Field(foreign_key='category.id')


class TransactionItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(default_factory=generate_uuid_str, nullable=False)
    sku: str
    quantidade: int
    transaction_id: int | None = Field(foreign_key='transaction.id')
    transaction: 'Transaction' = Relationship(back_populates='transacao_items')


class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(default_factory=generate_uuid_str, nullable=False)
    client_id: int | None = Field(foreign_key='client.id')
    dt_transacao: datetime = None
    dt_inclusao: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    dt_alteracao: datetime | None = None
    ativo: bool = True

    transacao_items: list[TransactionItem] = Relationship(
        back_populates='transaction'
    )


class StoreTransactions(SQLModel):
    client_id: int
    transactions: list[Transaction]


class AuthJwt(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    jti: str
    token_type: str
    revoked: bool = False
    expires: datetime

    client_id: int = Field(foreign_key='client.id')


class RegraCategoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tipo: str
    dt_inclusao: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    dt_alteracao: datetime | None = None
    categoria_id: int | None = Field(foreign_key='category.id')
    regra_id: int
    regra_id: int | None = Field(foreign_key='regra.id')
    regra: 'Regra' = Relationship(back_populates='regra_categorias')


class Regra(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    descricao_regra: str
    confianca: float
    suporte: float
    lift: float
    dt_alteracao: datetime | None = None
    ativo: bool = True
    regra_categorias: list[RegraCategoria] = Relationship(
        back_populates='regra', sa_relationship_kwargs={'cascade': 'delete'}
    )
    regra_run_id: int | None = Field(foreign_key='regrarun.id')


class RegraRun(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    min_support: float
    min_threshold: float
    metric: str
    dt_inclusao: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    client_id: int | None = Field(foreign_key='client.id')


class AlgoParams(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    min_support: float
    min_threshold: float
    metric: str
    dt_inclusao: datetime = Field(
        default_factory=datetime.utcnow, nullable=True
    )
    dt_alteracao: datetime | None = None
    client_id: int | None = Field(foreign_key='client.id')
