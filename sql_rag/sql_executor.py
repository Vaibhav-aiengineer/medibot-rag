import sqlite3

from sql_rag.sql_validator import (
    validate_sql
)


DB_PATH = "data/db/mediassist.db"


def execute_sql(sql):

    if not validate_sql(sql):

        raise ValueError(
            "SQL validation failed"
        )

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    try:

        cursor.execute(sql)

        columns = [
            desc[0]
            for desc in cursor.description
        ]

        rows = cursor.fetchall()

        return {
            "columns": columns,
            "rows": rows
        }

    finally:

        conn.close()


if __name__ == "__main__":

    sql = """
    SELECT COUNT(*) AS pending_claims
    FROM claims
    WHERE status='pending'
    """

    result = execute_sql(sql)

    print(result)