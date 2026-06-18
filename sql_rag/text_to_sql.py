from sql_rag.query_cache import (
    get_cached_sql,
    save_sql
)

from sql_rag.sql_generator import (
    generate_sql
)

from sql_rag.sql_executor import (
    execute_sql
)

from sql_rag.sql_formatter import (
    format_sql_answer
)




def run_text_to_sql(question):

    cached_sql = get_cached_sql(
        question
    )

    if cached_sql:

        print(
            "CACHE HIT"
        )

        sql = cached_sql

    else:

        print(
            "CACHE MISS"
        )

        sql = generate_sql(
            question
        )

        save_sql(
            question,
            sql
        )

    result = execute_sql(sql)

    answer = format_sql_answer(question,sql,result)

    return {"answer": answer,"sql": sql,"result": result}


if __name__ == "__main__":

    question = (
        "How many claims are pending?"
    )

    print("\nFIRST RUN\n")

    print(
        run_text_to_sql(question)
    )

    print("\nSECOND RUN\n")

    print(
        run_text_to_sql(question)
    )