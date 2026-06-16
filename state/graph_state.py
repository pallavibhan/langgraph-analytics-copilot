from typing import Annotated, TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    # This automatically tracks user prompts, assistant replies, 
    # and tool execution logs chronologically.
    messages: Annotated[List[BaseMessage], add_messages]
    subgroup_id: int