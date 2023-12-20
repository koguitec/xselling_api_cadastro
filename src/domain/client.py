"""Module for the client entity"""
import dataclasses
from typing import Dict

from src.domain.base import BaseDomainModel


@dataclasses.dataclass()
class Client(BaseDomainModel):
    """Client entity"""

    cnpj: str
    email: str
    razao_social: str

    @classmethod
    def from_dict(cls, d: Dict):
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

    def format_cnpj_with_special_caracters(self) -> str:
        """Format CNPJ without special characters

        Returns:
            self: CNPJ formatted with special characters
        """
        cnpj_clean = ''.join(char for char in self.cnpj if char.isdigit())

        formatted_cnpj = f'{cnpj_clean[:2]}.{cnpj_clean[2:5]}.{cnpj_clean[5:8]}/{cnpj_clean[8:12]}-{cnpj_clean[12:]}'

        self.cnpj = formatted_cnpj

        return self

    def format_cnpj_to_digits(self):
        """Format CNPJ with special characters

        Returns:
            dict: New dictionary with 'cnpj' key formatted containing no special characters
        """

        self.cnpj = (
            self.cnpj.replace('.', '').replace('/', '').replace('-', '')
        )

        return self
