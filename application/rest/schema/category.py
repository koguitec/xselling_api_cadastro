from pydantic import BaseModel


class Category(BaseModel):
    """Schema validatation for category"""

    descricao: str


class CategoryRequest(BaseModel):
    """Schema validatation for category"""

    categories: list[Category]

    class Config:
        extra = 'forbid'


class UpdateCategoryRequest(BaseModel):
    """Schema validatation for upadting a category"""

    id: int
    descricao: str
    ativo: bool

    class Config:
        extra = 'forbid'


class CategoryResponse(BaseModel):
    """Schema for category response"""

    id: int
    code: str
    descricao: str
    client_id: int
    dt_inclusao: str
    dt_alteracao: str
    ativo: bool


class CategoryResponseList(BaseModel):
    """Schema for category list response"""

    type: str
    count: int
    attributes: list[CategoryResponse]
