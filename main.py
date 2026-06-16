# from graph.workflow import graph
# from langchain_core.messages import HumanMessage
# import uuid

# def run():
#     session_id = str(uuid.uuid4())
#     config = {"configurable": {"thread_id": session_id}}
    
#     print("🤖 AI SQL Assistant initialized. Ask me anything! (Type 'exit' to quit)\n")
    
#     while True:
#         user_input = input("User: ")
#         if user_input.strip().lower() == "exit":
#             break
            
#         # Stream or invoke the updates through the loop
#         state_output = graph.invoke(
#             {"messages": [HumanMessage(content=user_input)], "subgroup_id": 289},
#             config=config
#         )
        
#         # The very last message in the graph state is the bot's latest response
#         latest_reply = state_output["messages"][-1].content
#         print(f"\nAssistant: {latest_reply}\n")

# if __name__ == "__main__":
#     run()

# main.py
# import uuid
# from graph.workflow import graph
# from langchain_core.messages import HumanMessage

# def run():
#     session_id = str(uuid.uuid4())
#     config = {"configurable": {"thread_id": session_id}}
    
#     print("🤖 Autonomous AI Data Analyst Initialized.")
    
#     # User se dynamic subgroup_id poochna
#     try:
#         subgroup_input = input("Enter Subgroup ID (e.g., 289): ").strip()
#         subgroup_id = int(subgroup_input)
#     except ValueError:
#         print("❌ Invalid Subgroup ID. Exiting.")
#         return

#     print(f"\nConnected to schema: subgroup_{subgroup_id}. Type 'exit' to quit.\n")
    
#     while True:
#         user_input = input("User: ")
#         if user_input.strip().lower() == "exit":
#             break
            
#         state_output = graph.invoke(
#             {
#                 "messages": [HumanMessage(content=user_input)], 
#                 "subgroup_id": subgroup_id
#             },
#             config=config
#         )
        
#         latest_reply = state_output["messages"][-1].content
#         print(f"\nAssistant:\n{latest_reply}\n")

# if __name__ == "__main__":
#     run()

import uuid
import asyncio
from graph.workflow import graph
from langchain_core.messages import HumanMessage

async def run_chat():
    session_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": session_id}}
    
    print("🤖 Autonomous AI Data Analyst Initialized (Streaming Enabled).")
    
    try:
        subgroup_input = input("Enter Subgroup ID (e.g., 289): ").strip()
        subgroup_id = int(subgroup_input)
    except ValueError:
        print("❌ Invalid Subgroup ID. Exiting.")
        return

    print(f"\nConnected to schema: subgroup_{subgroup_id}. Type 'exit' to quit.\n")
    
    while True:
        # Standard input directly works, no need for async input libraries for simple loops
        user_input = input("User: ")
        if user_input.strip().lower() == "exit":
            break
            
        print("\nAssistant: ", end="", flush=True)
        
        # graph.astream_events lagane se har ek token live capture hota hai
        async for event in graph.astream_events(
            {
                "messages": [HumanMessage(content=user_input)], 
                "subgroup_id": subgroup_id
            },
            config=config,
            version="v2"
        ):
            kind = event["event"]
            
            # Jab LLM internally text generate kar raha hota hai
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    # bina newline ke token print karna taaki live typing effect aaye
                    print(content, end="", flush=True)
        print("\n") # End of message spacing

def run():
    # Kyunki astream_events async hai, hum loop ko asyncio ke zariye run karenge
    asyncio.run(run_chat())

if __name__ == "__main__":
    run()