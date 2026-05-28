import sqlite3

from llm import llm


connection = sqlite3.connect(
    "database/soc_memory.db"
)

cursor = connection.cursor()


def get_recent_incidents():

    cursor.execute(
        """
        SELECT *
        FROM incidents
        ORDER BY id DESC
        LIMIT 10
        """
    )

    rows = cursor.fetchall()

    return rows


def soc_copilot(question):

    incidents = get_recent_incidents()

    context = "\n".join([
        str(row)
        for row in incidents
    ])


    prompt = f"""
    You are an expert SOC AI Copilot.

    Analyze the incidents and answer
    the analyst question.

    Recent Incidents:
    {context}

    Analyst Question:
    {question}

    Keep answer concise and professional.
    """

    response = llm.invoke(prompt)

    return response.content


while True:

    print("\n===== AI SOC COPILOT =====")

    question = input(
        "\nAsk Security Question: "
    )

    if question.lower() == "exit":
        break

    answer = soc_copilot(question)

    print("\n===== RESPONSE =====")
    print(answer)