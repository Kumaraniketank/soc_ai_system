from rag.retriever import retriever


def intelligence_agent(state):

    log = state["raw_log"]

    docs = retriever.invoke(log)

    intelligence = "\\n".join(
        [doc.page_content for doc in docs]
    )

    state["threat_intelligence"] = intelligence

    return state