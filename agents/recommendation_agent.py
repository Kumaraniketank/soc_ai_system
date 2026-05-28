from llm import llm


def recommendation_agent(state):

    threat = state["threat_type"]
    severity = state["severity"]

    prompt = f"""
    You are a cybersecurity response expert.

    Threat: {threat}
    Severity: {severity}

    Provide a recommended response.
    """

    response = llm.invoke(prompt)

    state["recommendation"] = response.content

    return state