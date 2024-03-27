from pydantic import BaseModel


class Product(BaseModel):
    """Schema validatation for product"""

    nome: str
    descricao: str
    sku: str
    categoria_id: int


class ProductRequest(BaseModel):
    """Schema validatation for product"""

    products: list[Product]

    class ConfigDict:
        extra = 'forbid'


class UpdateProductRequest(BaseModel):
    """Schema validatation for updating a product"""

    id: int
    nome: str
    descricao: str
    sku: str
    ativo: bool

    class ConfigDict:
        extra = 'forbid'


class ProductResponse(BaseModel):
    """Schema validation for product"""

    id: int
    code: str
    nome: str
    descricao: str
    sku: str
    categoria_id: int
    dt_inclusao: str
    dt_alteracao: str
    ativo: bool


class ProductResponseList(BaseModel):
    """Schema for category list response"""

    type: str
    count: int
    attributes: list[ProductResponse]
