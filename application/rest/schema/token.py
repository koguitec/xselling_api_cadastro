from pydantic import BaseModel


class TokenData(BaseModel):
    client_id: str | None = None

    class ConfigDict:
        extra = 'forbid'
