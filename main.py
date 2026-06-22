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


#----------------------------------------------v2---------------------------
# import uuid
# import asyncio
# from graph.workflow import graph
# from langchain_core.messages import HumanMessage

# async def run_chat():
#     session_id = str(uuid.uuid4())
#     config = {"configurable": {"thread_id": session_id}}
    
#     print("🤖 Autonomous AI Data Analyst Initialized (Streaming Enabled).")
    
#     try:
#         subgroup_input = input("Enter Subgroup ID (e.g., 289): ").strip()
#         subgroup_id = int(subgroup_input)
#     except ValueError:
#         print("❌ Invalid Subgroup ID. Exiting.")
#         return

#     print(f"\nConnected to schema: subgroup_{subgroup_id}. Type 'exit' to quit.\n")
    
#     while True:
#         # Standard input directly works, no need for async input libraries for simple loops
#         user_input = input("User: ")
#         if user_input.strip().lower() == "exit":
#             break
            
#         print("\nAssistant: ", end="", flush=True)
        
#         # graph.astream_events lagane se har ek token live capture hota hai
#         async for event in graph.astream_events(
#             {
#                 "messages": [HumanMessage(content=user_input)], 
#                 "subgroup_id": subgroup_id
#             },
#             config=config,
#             version="v2"
#         ):
#             kind = event["event"]
            
#             # Jab LLM internally text generate kar raha hota hai
#             if kind == "on_chat_model_stream":
#                 content = event["data"]["chunk"].content
#                 if content:
#                     # bina newline ke token print karna taaki live typing effect aaye
#                     print(content, end="", flush=True)
#         print("\n") # End of message spacing

# def run():
#     # Kyunki astream_events async hai, hum loop ko asyncio ke zariye run karenge
#     asyncio.run(run_chat())

# if __name__ == "__main__":
#     run()

#----------------------------------v3---------------------------------

# import uuid
# import asyncio
# import sys
# from graph.workflow import graph
# from langchain_core.messages import HumanMessage

# # Global spinner control karne ke liye task list
# spinner_task = None

# async def spin_loading(message="Fetching data from Trino Database... Please wait"):
#     """Background task jo console me moving/rotating spinner dikhayega"""
#     # Moving animation ke characters
#     spinner_symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
#     idx = 0
#     try:
#         while True:
#             # \r lagane se cursor line ke start me chala jata h aur text overwrite hota h (movement effect)
#             sys.stdout.write(f"\r{spinner_symbols[idx]} [{message}] ")
#             sys.stdout.flush()
#             idx = (idx + 1) % len(spinner_symbols)
#             await asyncio.sleep(0.1) # Movement ki speed
#     except asyncio.CancelledError:
#         # Jab task cancel hoga (yaani tool end hoga), toh line ko saaf kar denge
#         sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
#         sys.stdout.flush()

# async def run_chat():
#     global spinner_task
#     session_id = str(uuid.uuid4())
#     config = {"configurable": {"thread_id": session_id}}
    
#     print("🤖 Autonomous AI Data Analyst Initialized (Streaming Enabled).")
    
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
            
#         print("\nAssistant: ", end="", flush=True)
        
#         # graph.astream_events lagane se har ek event live capture hota hai
#         async for event in graph.astream_events(
#             {
#                 "messages": [HumanMessage(content=user_input)], 
#                 "subgroup_id": subgroup_id
#             },
#             config=config,
#             version="v2"
#         ):
#             kind = event["event"]
            
#             # 1. JAISE HI TOOL SHURU HO -> Background me moving spinner task start kar do
#             if kind == "on_tool_start":
#                 tool_name = event["name"]
#                 msg = "Fetching data from Trino Database... Please wait"
#                 if tool_name == "save_to_markdown":
#                     msg = "Generating Markdown Report..."
                
#                 # Agar pehle se koi spinner chal rha h toh band karo (safeguard)
#                 if spinner_task and not spinner_task.done():
#                     spinner_task.cancel()
                
#                 # New moving loader task ko start karo
#                 spinner_task = asyncio.create_task(spin_loading(msg))
            
#             # 2. JAISE IN TOOL KHATAM HO -> Spinner task ko cancel karo aur "Done" print karo
#             elif kind == "on_tool_end":
#                 if spinner_task and not spinner_task.done():
#                     spinner_task.cancel()
#                     await asyncio.sleep(0.05) # Loader ko cancel hone ka thoda waqt do
#                 print("✅ Done.", flush=True)
            
#             # 3. Jab LLM internally text generate kar raha hota hai (streaming tokens)
#             elif kind == "on_chat_model_stream":
#                 content = event["data"]["chunk"].content
#                 if content:
#                     # Bina newline ke token print karna taaki live typing effect aaye
#                     print(content, end="", flush=True)
                    
#         print("\n") # End of message spacing

# def run():
#     # Kyunki astream_events async hai, hum loop ko asyncio ke zariye run karenge
#     asyncio.run(run_chat())

# if __name__ == "__main__":
#     run()



#---------------------------------------v4--------------------------------------------------------------------------------------------------------------------------    





# import uuid
# import asyncio
# import sys
# from graph.workflow import graph
# from langchain_core.messages import HumanMessage

# # Global spinner control karne ke liye task list
# spinner_task = None

# async def spin_loading(message="Fetching data from Trino Database... Please wait"):
#     """Background task jo console me moving/rotating spinner dikhayega"""
#     spinner_symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
#     idx = 0
#     try:
#         while True:
#             sys.stdout.write(f"\r{spinner_symbols[idx]} [{message}] ")
#             sys.stdout.flush()
#             idx = (idx + 1) % len(spinner_symbols)
#             await asyncio.sleep(0.1)
#     except asyncio.CancelledError:
#         sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
#         sys.stdout.flush()

# async def run_chat():
#     global spinner_task
#     session_id = str(uuid.uuid4())
#     config = {"configurable": {"thread_id": session_id}}
    
#     # Global rates for GPT-5.4 mini
#     fresh_rate = 0.75 / 1000000
#     cached_rate = 0.075 / 1000000
#     output_rate = 4.50 / 1000000
    
#     print("🤖 Autonomous AI Data Analyst Initialized (Streaming Enabled).")
    
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
            
#         print("\nAssistant: ", end="", flush=True)
        
#         # graph.astream_events lagane se har ek event live capture hota hai
#         async for event in graph.astream_events(
#             {
#                 "messages": [HumanMessage(content=user_input)], 
#                 "subgroup_id": subgroup_id
#             },
#             config=config,
#             version="v2"
#         ):
#             kind = event["event"]
            
#             # 1. JAISE HI TOOL SHURU HO -> Background me moving spinner task start kar do
#             if kind == "on_tool_start":
#                 tool_name = event["name"]
#                 msg = "Fetching data from Trino Database... Please wait"
#                 if tool_name == "save_to_markdown":
#                     msg = "Generating Markdown Report..."
                
#                 if spinner_task and not spinner_task.done():
#                     spinner_task.cancel()
                
#                 spinner_task = asyncio.create_task(spin_loading(msg))
            
#             # 2. JAISE IN TOOL KHATAM HO -> Spinner task ko cancel karo aur "Done" print karo
#             elif kind == "on_tool_end":
#                 if spinner_task and not spinner_task.done():
#                     spinner_task.cancel()
#                     await asyncio.sleep(0.05)
#                 print("✅ Done.", flush=True)
            
#             # 3. Jab LLM internally text generate kar raha hota hai (streaming tokens)
#             elif kind == "on_chat_model_stream":
#                 content = event["data"]["chunk"].content
#                 if content:
#                     print(content, end="", flush=True)

#             # 4. 🔥 REAL-TIME TOKEN & PRICING TRACKING (Har LLM call ke khatam hone par)
#             elif kind == "on_chat_model_end":
#                 try:
#                     output_data = event["data"].get("output", {})
#                     # Handle both Message chunk or standard structure safely
#                     usage = getattr(output_data, "usage_metadata", None)
                    
#                     if usage:
#                         input_tokens = usage.get("input_tokens", 0)
#                         output_tokens = usage.get("output_tokens", 0)
#                         total_tokens = usage.get("total_tokens", 0)
                        
#                         input_details = usage.get("input_token_details", {})
#                         cache_tokens = input_details.get("cached", 0) if input_details else 0
#                         fresh_input_tokens = input_tokens - cache_tokens
                        
#                         # Pricing Calculations
#                         cost_fresh = fresh_input_tokens * fresh_rate
#                         cost_cached = cache_tokens * cached_rate
#                         cost_output = output_tokens * output_rate
#                         total_cost = cost_fresh + cost_cached + cost_output
                        
#                         # Output screen par metrics flash karna
#                         print("\n\n==============================================")
#                         print("📊 REAL-TIME LLM STEP COST & TOKEN METRICS")
#                         print("==============================================")
#                         print(f"🔹 Context Inputs   : {input_tokens} [Fresh: {fresh_input_tokens} | Cached: {cache_tokens} ⚡]")
#                         print(f"🔹 Model Outputs    : {output_tokens}")
#                         print(f"🔹 Total Transacted : {total_tokens}")
#                         print(f"💵 Transaction Cost : ${total_cost:.6f}")
#                         print("==============================================\n")
#                 except Exception as e:
#                     pass # Safeguard against parsing anomalies
                    
#         print("\n") # End of message spacing

# def run():
#     asyncio.run(run_chat())

# if __name__ == "__main__":
#     run()


# --------------------------------------------------v5----------------------------------------------------------------------------------------------------------------------



import uuid
import asyncio
import sys
from graph.workflow import graph
from langchain_core.messages import HumanMessage

# Global spinner control karne ke liye task list
spinner_task = None

async def spin_loading(message="Fetching data from Trino Database... Please wait"):
    """Background task jo console me moving/rotating spinner dikhayega"""
    spinner_symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    idx = 0
    try:
        while True:
            sys.stdout.write(f"\r{spinner_symbols[idx]} [{message}] ")
            sys.stdout.flush()
            idx = (idx + 1) % len(spinner_symbols)
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
        sys.stdout.flush()

async def run_chat():
    global spinner_task
    session_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": session_id}}
    
    # Global rates for GPT-5.4 mini (Per 1 Million tokens)
    fresh_rate = 0.75 / 1000000
    cached_rate = 0.075 / 1000000
    output_rate = 4.50 / 1000000
    
    print("🤖 Autonomous AI Data Analyst Initialized (Streaming Enabled).")
    
    try:
        subgroup_input = input("Enter Subgroup ID (e.g., 289): ").strip()
        subgroup_id = int(subgroup_input)
    except ValueError:
        print("❌ Invalid Subgroup ID. Exiting.")
        return

    print(f"\nConnected to schema: subgroup_{subgroup_id}. Type 'exit' to quit.\n")
    
    while True:
        user_input = input("User: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "exit":
            break
            
        print("\nAssistant: ", end="", flush=True)
        
        # graph.astream_events lagane se har ek event live capture hota hai
        async for event in graph.astream_events(
            {
                "messages": [HumanMessage(content=user_input)], 
                "subgroup_id": subgroup_id
            },
            config=config,
            version="v2"
        ):
            kind = event["event"]
            
            # 1. JAISE HI TOOL SHURU HO -> Loader shuru karo
            if kind == "on_tool_start":
                tool_name = event["name"]
                msg = "Fetching data from Trino Database... Please wait"
                if tool_name == "save_to_markdown":
                    msg = "Generating Markdown Report..."
                
                if spinner_task and not spinner_task.done():
                    spinner_task.cancel()
                
                spinner_task = asyncio.create_task(spin_loading(msg))
            
            # 2. JAISE HI TOOL KHATAM HO -> Loader band karke Done bolo
            elif kind == "on_tool_end":
                if spinner_task and not spinner_task.done():
                    spinner_task.cancel()
                    await asyncio.sleep(0.05)
                print("✅ Done.", flush=True)
            
            # 3. Jab LLM internally text generate kar raha hota hai (streaming chunks)
            elif kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    print(content, end="", flush=True)

            # 4. 🔥 HAR STEP KE END ME EXACTLY NEECHE METRICS DIKHANA
            elif kind == "on_chat_model_end":
                try:
                    output_data = event["data"].get("output", {})
                    usage = getattr(output_data, "usage_metadata", None)
                    
                    if usage:
                        input_tokens = usage.get("input_tokens", 0)
                        output_tokens = usage.get("output_tokens", 0)
                        total_tokens = usage.get("total_tokens", 0)
                        
                        input_details = usage.get("input_token_details", {})
                        cache_tokens = input_details.get("cached", 0) if input_details else 0
                        fresh_input_tokens = input_tokens - cache_tokens
                        
                        # Pricing Calculations
                        cost_fresh = fresh_input_tokens * fresh_rate
                        cost_cached = cache_tokens * cached_rate
                        cost_output = output_tokens * output_rate
                        total_cost = cost_fresh + cost_cached + cost_output
                        
                        # Force formatting newline taaki mix na ho
                        print("\n")
                        print("==========================================================")
                        print("📊 STEP METRICS REPORT (GPT-5.4 mini)")
                        print("==========================================================")
                        print(f"🔹 Context Inputs   : {input_tokens} [Fresh: {fresh_input_tokens} | Cached: {cache_tokens} ⚡]")
                        print(f"🔹 Model Outputs    : {output_tokens}")
                        print(f"🔹 Total Transacted : {total_tokens}")
                        print(f"💵 Transaction Cost : ${total_cost:.6f}")
                        print("==========================================================\n")
                except Exception as e:
                    pass
                    
        print("\n") # Har conversation turn ke baad spacing

def run():
    asyncio.run(run_chat())

if __name__ == "__main__":
    run()