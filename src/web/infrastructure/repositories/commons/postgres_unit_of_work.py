from typing import ContextManager

from ddd.unit_of_work import IUnitOfWork
from django.db import transaction


class PostgresUnitOfWork(IUnitOfWork):
    def atomic(self) -> ContextManager[None]:
        return transaction.atomic()
