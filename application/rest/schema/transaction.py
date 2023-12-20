from datetime import datetime

from pydantic import BaseModel


class Product(BaseModel):
    sku: str
    quantidade: int


class Transaction(BaseModel):
    dt_transacao: datetime
    transacao_items: list[Product]


class StoreTransactions(BaseModel):
    transacoes: list[Transaction]

    class ConfigDict:
        extra = 'forbid'
