from typing import Optional

from pydantic import BaseModel


class ProductSchema(BaseModel):
    """Schema validatation for product"""

    nome: str
    descricao: str
    sku: str
    categoria_id: int

    class ConfigDict:
        extra = 'forbid'


class UpdateProductSchema(BaseModel):
    """Schema validatation for updating a product"""

    id: int
    code: Optional[str]
    nome: Optional[str]
    descricao: Optional[str]
    sku: Optional[str]
    ativo: Optional[str]

    class ConfigDict:
        extra = 'forbid'
