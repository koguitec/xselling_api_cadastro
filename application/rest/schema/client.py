from pydantic import BaseModel, EmailStr, constr


class ClientRequest(BaseModel):
    """Schema validation for Client"""

    razao_social: str
    cnpj: constr(pattern=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$')
    email: EmailStr

    class ConfigDict:
        extra = 'forbid'


class UpdateClientSchema(BaseModel):
    """Schema validation for Client"""

    id: int
    razao_social: str
    cnpj: str
    email: str
    ativo: bool

    class ConfigDict:
        extra = 'forbid'


class ClientResponse(BaseModel):
    """Schema validation for Client"""

    id: int
    code: str
    razao_social: str
    cnpj: str
    email: str
    dt_inclusao: str
    dt_alteracao: str
    ativo: bool


class ClientResponseList(BaseModel):
    """Schema for category list response"""

    type: str
    count: int
    attributes: list[ClientResponse]
