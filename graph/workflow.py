# from langgraph.graph import StateGraph, END
# from langgraph.prebuilt import ToolNode, tools_condition
# from state.graph_state import GraphState
# from agents.query_bot import query_agent_node
# from tools.sql_tool import ask_database
# from tools.file_tool import save_to_markdown
# from memory.memory_manager import memory

# builder = StateGraph(GraphState)

# # Define our two structural nodes
# builder.add_node("query_agent", query_agent_node)
# builder.add_node("tools", ToolNode([ask_database, save_to_markdown]))

# builder.set_entry_point("query_agent")

# # CONDITIONAL ROUTER: 
# # If the LLM output wants to call a tool, it goes to "tools".
# # If the LLM just replied with text (clarifying question or final answer), it ends the turn.
# builder.add_conditional_edges(
#     "query_agent",
#     tools_condition
# )

# # Static edge to loop tool data back into the agent context
# builder.add_edge("tools", "query_agent")

# graph = builder.compile(checkpointer=memory)

#===========================nnnnnnn====================================================

# from langgraph.graph import StateGraph, END
# from langgraph.prebuilt import ToolNode, tools_condition
# from state.graph_state import GraphState
# from agents.query_bot import query_agent_node
# from memory.memory_manager import memory

# def create_graph(mcp_tools):
#     """
#     Dynamic LangGraph workflow jo runtime par MCP server se fetched tools ko state me bind karta hai.
#     """
#     builder = StateGraph(GraphState)

#     # 1. Structural Nodes Register Karein
#     builder.add_node("query_agent", query_agent_node)
    
#     # Ab ToolNode local python functions ki jagah runtime dynamic MCP tools use karega
#     builder.add_node("tools", ToolNode(mcp_tools))

#     # 2. Entry Point Setup Karein
#     builder.set_entry_point("query_agent")

#     # 3. Conditional Router Edges
#     # Agar LLM tool call generate karega toh "tools" node par jayega, warna END hoga
#     builder.add_conditional_edges(
#         "query_agent",
#         tools_condition
#     )

#     # 4. Loop back edge to resubmit tool results back to LLM context
#     builder.add_edge("tools", "query_agent")

#     # Final Graph compilation persistent memory checkpoint saver ke sath
#     return builder.compile(checkpointer=memory)


#===================================nnnnnnnnnnnnnnnnnnnn=====================

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from state.graph_state import GraphState
from memory.memory_manager import memory

def create_graph(mcp_tools):
    """
    Dynamic LangGraph workflow jo runtime par inject hue combined tools ko state context me pass karta hai.
    """
    builder = StateGraph(GraphState)

    # Injected tools ko direct agent context state me inject karne ke liye node wrapper
    async def agent_execution_node(state):
        # Tools array ko state me inject kar diya taaki query_bot use read kar sake
        state["mcp_tools"] = mcp_tools
        from agents.query_bot import query_agent_node
        return await query_agent_node(state)

    builder.add_node("query_agent", agent_execution_node)
    builder.add_node("tools", ToolNode(mcp_tools))

    builder.set_entry_point("query_agent")
    builder.add_conditional_edges("query_agent", tools_condition)
    builder.add_edge("tools", "query_agent")

    return builder.compile(checkpointer=memory)