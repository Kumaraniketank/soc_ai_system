from database.db import cursor


def memory_lookup_agent(state):

    parsed = state["parsed_log"]

    ip = parsed.get("ip_address")

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM incidents
        WHERE ip_address = ?
        """,
        (ip,)
    )

    count = cursor.fetchone()[0]

    state["previous_incidents"] = count

    return state