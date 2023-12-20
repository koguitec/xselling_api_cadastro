from typing import Optional

from pydantic import BaseModel


class CategorySchema(BaseModel):
    """Schema validatation for category"""

    descricao: str
    client_id: int

    class ConfigDict:
        extra = 'forbid'


class UpdateCategorySchema(BaseModel):
    """Schema validatation for upadting a category"""

    id: int
    code: Optional[str]
    descricao: Optional[str]
    ativo: Optional[bool]

    class ConfigDict:
        extra = 'forbid'
