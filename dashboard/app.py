import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px


st.set_page_config(
    page_title="AI SOC Dashboard",
    layout="wide"
)

st.title("Real-Time AI SOC Dashboard")


connection = sqlite3.connect(
    "database/soc_memory.db"
)

query = """
SELECT *
FROM incidents
ORDER BY timestamp DESC
"""

df = pd.read_sql(query, connection)


st.subheader("Recent Incidents")

st.dataframe(df, use_container_width=True)


if not df.empty:

    severity_counts = (
        df["severity"]
        .value_counts()
        .reset_index()
    )

    severity_counts.columns = [
        "Severity",
        "Count"
    ]

    fig = px.bar(
        severity_counts,
        x="Severity",
        y="Count",
        title="Incident Severity Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Recent Critical Incidents")

    critical_df = df[
        df["severity"].str.contains(
            "CRITICAL",
            case=False,
            na=False
        )
    ]

    st.dataframe(
        critical_df,
        use_container_width=True
    )

else:

    st.warning("No incidents detected yet")