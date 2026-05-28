from langgraph.graph import StateGraph, END

from graphs.state import SOCState

from agents.parser_agent import parser_agent
from agents.intelligent_agent import intelligence_agent
from agents.threat_agent import threat_agent
from agents.severity_agent import severity_agent
from agents.recommendation_agent import recommendation_agent
from agents.correlation_agent import correlation_agent
from agents.response_agent import response_agent
from agents.report_agent import report_agent


# =========================================
# CREATE GRAPH
# =========================================

workflow = StateGraph(SOCState)


# =========================================
# ADD NODES
# =========================================

workflow.add_node(
    "parser",
    parser_agent
)

workflow.add_node(
    "intelligence",
    intelligence_agent
)

workflow.add_node(
    "threat",
    threat_agent
)

workflow.add_node(
    "severity",
    severity_agent
)

workflow.add_node(
    "recommendation",
    recommendation_agent
)

workflow.add_node(
    "correlation",
    correlation_agent
)

workflow.add_node(
    "response",
    response_agent
)

workflow.add_node(
    "report",
    report_agent
)


# =========================================
# ENTRY POINT
# =========================================

workflow.set_entry_point(
    "parser"
)


# =========================================
# FLOW
# =========================================

workflow.add_edge(
    "parser",
    "intelligence"
)

workflow.add_edge(
    "intelligence",
    "threat"
)

workflow.add_edge(
    "threat",
    "severity"
)

workflow.add_edge(
    "severity",
    "recommendation"
)

workflow.add_edge(
    "recommendation",
    "correlation"
)

workflow.add_edge(
    "correlation",
    "response"
)

workflow.add_edge(
    "response",
    "report"
)

workflow.add_edge(
    "report",
    END
)


# =========================================
# COMPILE
# =========================================

workflow = workflow.compile()