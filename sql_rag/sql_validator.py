from sql_rag.config import (
    ALLOWED_TABLES
)


def validate_sql(sql):

    sql_upper = sql.strip().upper()

    # Only SELECT allowed
    if not sql_upper.startswith(
        "SELECT"
    ):
        return False

    # Dangerous keywords
    blocked_keywords = [

        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE"

    ]

    for keyword in blocked_keywords:

        if keyword in sql_upper:
            return False

    # Table whitelist
    table_found = False

    for table in ALLOWED_TABLES:

        if table in sql.lower():

            table_found = True

            break

    if not table_found:

        return False

    return True

if __name__ == "__main__":

    sql = """
    SELECT COUNT(*)
    FROM claims
    """

    print(
        validate_sql(sql)
    )