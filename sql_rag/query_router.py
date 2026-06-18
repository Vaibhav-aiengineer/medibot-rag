ANALYTICAL_KEYWORDS = [

    "count",
    "how many",
    "average",
    "avg",
    "sum",
    "total",
    "highest",
    "lowest",
    "most",
    "least",
    "top",
    "maximum",
    "minimum"

]


def is_sql_question(question):

    question = question.lower()

    return any(
        keyword in question
        for keyword in ANALYTICAL_KEYWORDS
    )