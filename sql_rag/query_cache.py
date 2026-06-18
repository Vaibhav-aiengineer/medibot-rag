QUERY_CACHE = {}


def get_cached_sql(question):

    return QUERY_CACHE.get(
        question.lower().strip()
    )


def save_sql(question, sql):

    QUERY_CACHE[
        question.lower().strip()
    ] = sql