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
    nome: str
    descricao: str
    sku: str
    ativo: str

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
