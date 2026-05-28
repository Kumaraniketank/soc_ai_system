from database.db import cursor, connection


def memory_update_agent(state):

    parsed = state["parsed_log"]

    cursor.execute(
        """
        INSERT INTO incidents (
            ip_address,
            event_type,
            threat_type,
            severity
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            parsed["ip_address"],
            parsed["event"],
            state["threat_type"],
            state["severity"]
        )
    )

    connection.commit()

    return state