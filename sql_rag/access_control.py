from sql_rag.config import (
    SQL_ALLOWED_ROLES
)


def can_use_sql(role):

    return role in SQL_ALLOWED_ROLES