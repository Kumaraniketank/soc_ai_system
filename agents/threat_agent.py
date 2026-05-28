from llm import llm


def threat_agent(state):

    log = state["raw_log"]

    intelligence = state.get(
        "threat_intelligence",
        "No threat intelligence available."
    )

    parsed_log = state.get(
        "parsed_log",
        {}
    )

    prompt = f"""
    You are an expert SOC analyst.

    Analyze the security event carefully.

    Threat Intelligence:
    {intelligence}

    Parsed Security Data:
    {parsed_log}

    Raw Security Log:
    {log}

    Your task:
    1. Identify likely attack type
    2. Identify important indicators
    3. Explain threat briefly
    4. Mention confidence level

    Rules:
    - Be concise
    - Avoid guessing
    - If evidence is weak, say "Suspicious Activity"
    - Focus on cybersecurity relevance only
    """

    try:

        response = llm.invoke(prompt)

        state["threat_type"] = response.content

    except Exception as e:

        print("Threat Agent Error:", e)

        state["threat_type"] = """
        Attack type: Suspicious Activity

        Indicators:
        - Unable to fully analyze log

        Threat summary:
        LLM analysis temporarily unavailable.

        Confidence: Low
        """

    return state