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


