import dataclasses
from datetime import datetime
from enum import Enum


class TokenTypeEnum(Enum):
    REFRESH = 'refresh'


@dataclasses.dataclass
class AuthJwt:
    jti: str
    client_id: int
    token_type: TokenTypeEnum = 'refresh'
    revoked: bool = False
    id: int | None = None
    expires: datetime = None

    @classmethod
    def from_dict(cls, d):
        """Initialize an object from a dictionary

        Args:
            d (Dict): dictionary containing all class attributes

        Returns:
            Model: Instance of class object
        """
        return cls(**d)

    def to_dict(self):
        """Returns a dictinary from a class object

        Returns:
            Dict: dictionary containg all class attribute data
        """
        return dataclasses.asdict(self)
