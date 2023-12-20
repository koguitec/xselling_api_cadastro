# pylint: disable=c0103
# pylint: disable=c0209
# pylint: disable=c0116
from src.domain.transaction import Transaction
from src.repository.postgres.base_postgresrepo import BasePostgresRepo
from src.repository.postgres.postgres_objects import StoreTransactions
from src.repository.postgres.postgres_objects import (
    Transaction as PgTransaction,
)
from src.repository.postgres.postgres_objects import (
    TransactionItem as PgTransactionItem,
)


class PostgresRepoTransaction(BasePostgresRepo):
    """Postgres Transaction repository"""

    def __init__(self) -> None:
        super().__init__()

    def _create_transaction_objects(
        self, result: list[PgTransaction]
    ) -> list[Transaction]:
        return [
            Transaction(
                id=t.id,
                code=t.code,
                dt_inclusao=t.dt_inclusao,
                dt_alteracao=t.dt_alteracao,
                dt_transacao=t.dt_transacao,
                client_id=t.client_id,
                ativo=t.ativo,
            )
            for t in result
        ]

    def list_transaction(self, filters=None) -> list[Transaction]:
        session = self._create_session()

        query = session.query(PgTransaction)

        if filters is None:
            return self._create_transaction_objects(query.all())

        if 'id__eq' in filters:
            query = query.filter(PgTransaction.id == filters['id__eq'])

        if 'code__eq' in filters:
            query = query.filter(PgTransaction.code == filters['code__eq'])

        if 'ativo__eq' in filters:
            query = query.filter(PgTransaction.ativo == filters['ativo__eq'])

        if 'client_id__eq' in filters:
            query = query.filter(
                PgTransaction.client_id == filters['client_id__eq']
            )

        if 'produto_id__eq' in filters:
            query = query.filter(
                PgTransaction.produto_id == filters['produto_id__eq']
            )

        return self._create_transaction_objects(query.all())

    def create_transaction(self, new_transaction: dict):
        session = self._create_session()

        try:
            for transaction in new_transaction['transactions']:
                db_transaction = PgTransaction(
                    # code=transaction["code"],
                    client_id=new_transaction['client_id'],
                    dt_transacao=transaction['dt_transacao'],
                )
                session.add(db_transaction)
                session.flush()

                for item in transaction['transacao_items']:
                    db_item = PgTransactionItem(
                        # code=item["code"],
                        sku=item['sku'],
                        quantidade=item['quantidade'],
                        transaction_id=db_transaction.id,
                    )
                    session.add(db_item)
        except:
            session.rollback()
            raise
        else:
            session.commit()

        # TODO retornar alguma informação, ex: número de transações adicionadas
