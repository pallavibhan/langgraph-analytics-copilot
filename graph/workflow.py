from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from state.graph_state import GraphState
from agents.query_bot import query_agent_node
from tools.sql_tool import ask_database
from tools.file_tool import save_to_markdown
from memory.memory_manager import memory

builder = StateGraph(GraphState)

# Define our two structural nodes
builder.add_node("query_agent", query_agent_node)
builder.add_node("tools", ToolNode([ask_database, save_to_markdown]))

builder.set_entry_point("query_agent")

# CONDITIONAL ROUTER: 
# If the LLM output wants to call a tool, it goes to "tools".
# If the LLM just replied with text (clarifying question or final answer), it ends the turn.
builder.add_conditional_edges(
    "query_agent",
    tools_condition
)

# Static edge to loop tool data back into the agent context
builder.add_edge("tools", "query_agent")

graph = builder.compile(checkpointer=memory)