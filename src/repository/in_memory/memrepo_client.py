"""Module for the Client in memory repository"""
import uuid
from typing import Dict, List

from src.domain.client import Client


class MemRepo:
    """Class for the Client in memory repository"""

    def __init__(self, data: List[Dict]) -> None:
        self.data = data

    def list_client(self, filters: {} = None) -> List:
        """List all clients

        Returns:
            List: List of client objectcs
        """
        result = [Client.from_dict(c) for c in self.data]

        if filters is None:
            return result

        if 'code__eq' in filters:
            result = [c for c in result if c.code == filters['code__eq']]

        if 'ativo__eq' in filters:
            result = [
                c
                for c in result
                if c.ativo is (filters['ativo__eq'] == 'true')
            ]

        return result

    def get_client_by_code(self, code: str) -> Dict:
        """Retrive client information

        Args:
            code (str): _description_

        Returns:
            Client: _description_
        """

        return [c for c in self.data if c['code'] == code][0]

    def create_client(self, client: Client) -> None:
        """Creates a client

        Args:
            client (Client): Client object
        """
        client.update({'code': str(uuid.uuid4())})
        self.data.append(client)

        return client

    def update_client(self, new_client_data: Dict) -> Dict:
        """Updates client information

        Args:
            client (Client): Client object

        Returns:
            Client: Updated client object
        """
        for client in self.data:
            if client['code'] == new_client_data['code']:
                client.update(new_client_data)

                return client
