from llm import llm


def severity_agent(state):

    threat = state["threat_type"]

    previous_incidents = state["previous_incidents"]

    prompt = f"""
    You are a cybersecurity severity analyzer.

    Threat:
    {threat}

    Previous incidents from same source:
    {previous_incidents}

    Rules:
    - repeated attacks increase severity
    - persistent attacks are dangerous

    Classify severity as:
    LOW
    MEDIUM
    HIGH
    CRITICAL

    Return only severity label.
    """

    response = llm.invoke(prompt)

    state["severity"] = response.content.strip()

    return state