from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class ClientSchema(BaseModel):
    """Schema validation for Client"""

    razao_social: str
    cnpj: constr(pattern=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$')
    email: EmailStr

    class ConfigDict:
        extra = 'forbid'


class UpdateClientSchema(BaseModel):
    """Schema validation for Client"""

    id: int
    code: Optional[str]
    razao_social: Optional[str]
    cnpj: Optional[str]
    email: Optional[str]
    ativo: Optional[bool]

    class ConfigDict:
        extra = 'forbid'
