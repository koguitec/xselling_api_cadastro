from datetime import datetime

from pydantic import BaseModel


class Product(BaseModel):
    sku: str
    quantidade: int


class Transaction(BaseModel):
    dt_transacao: datetime
    transacao_items: list[Product]


class TransactionRequest(BaseModel):
    transacoes: list[Transaction]

    class ConfigDict:
        extra = 'forbid'


class TransactionResponse(BaseModel):
    id: int
    code: str
    cliente_id: int
    dt_transacao: str
    dt_inclusao: str
    data_alteracao: str
    ativo: bool


class TransactionResponseList(BaseModel):
    """Schema for category list response"""

    type: str
    count: int
    attributes: list[TransactionResponse]
