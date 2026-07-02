

import uuid
import asyncio
import sys
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Import official MCP communication components
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

# LangChain toolkit adapter for Model Context Protocol
from langchain_mcp import MCPToolkit
from agents.query_bot import model
# Dynamic graph compiler
from graph.workflow import create_graph

load_dotenv()
PRICING_TABLE = {
    "gpt-4o": {
        "fresh_rate": 2.50 / 1000000,
        "cached_rate": 1.25 / 1000000,
        "output_rate": 10.00 / 1000000
    },
    "gpt-4o-mini": {
        "fresh_rate": 0.150 / 1000000,
        "cached_rate": 0.075 / 1000000,
        "output_rate": 0.600 / 1000000
    },
    "claude-3-5-sonnet": {
        "fresh_rate": 3.00 / 1000000,
        "cached_rate": 0.30 / 1000000,
        "output_rate": 15.00 / 1000000
    },
    # Fallback default rates configuration rules (Aapke original values)
    "gpt-5.4-mini": {
        "fresh_rate": 0.75 / 1000000,
        "cached_rate": 0.075 / 1000000,
        "output_rate": 4.50 / 1000000
    }
}

spinner_task = None

async def spin_loading(message="Fetching data from Trino Database... Please wait"):
    """Background task that provides a rotating terminal spinner for active tool loops."""
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


    
    
    # Pricing rates configuration rules
    # fresh_rate = 0.75 / 1000000
    # cached_rate = 0.075 / 1000000
    # output_rate = 4.50 / 1000000

    pricing = PRICING_TABLE.get(
        model.model_name,
        PRICING_TABLE["gpt-5.4-mini"]  # fallback model
    )

    fresh_rate = pricing["fresh_rate"]
    cached_rate = pricing["cached_rate"]
    output_rate = pricing["output_rate"]
    
    print("🤖 Autonomous AI Data Analyst Initialized (Dual Transport MCP Enabled).")
    
    try:
        subgroup_input = input("Enter Subgroup ID (e.g., 289): ").strip()
        subgroup_id = int(subgroup_input)
    except ValueError:
        print("❌ Invalid Subgroup ID. Exiting.")
        return

    # =========================================================================
    # 🔌 TRANSPORT 1: LOCAL STDIO SERVER (Database Queries Engine)
    # =========================================================================
    # FIX: Windows aur virtual environment (.venv) issues se bachne ke liye sys.executable use kiya hai
    stdio_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server.py"],  # Executes your standard ask_database tool
        env=os.environ.copy()
    )

    # =========================================================================
    # 🔌 TRANSPORT 2: REMOTE HTTP SSE OAUTH SERVER (Report File Generator Engine)
    # =========================================================================
    # Official FastMCP native routing structures bind standard endpoints under /sse
    remote_sse_url = os.getenv("REMOTE_MCP_SSE_URL", "http://127.0.0.1:8000/sse")
    oauth_token = os.getenv("REMOTE_MCP_OAUTH_TOKEN", "valid_mock_token_123")
    sse_headers = {"Authorization": f"Bearer {oauth_token}"}

    print("\n🔌 Establishing concurrent handshakes with Stdio and HTTP SSE OAuth servers...")
    
    # 1. Nest Local Stdio Server Connection Pipeline
    async with stdio_client(stdio_params) as (stdio_read, stdio_write):
        async with ClientSession(stdio_read, stdio_write) as stdio_session:
            await stdio_session.initialize()
            
            stdio_toolkit = MCPToolkit(session=stdio_session)
            await stdio_toolkit.initialize()
            database_tools = stdio_toolkit.get_tools()
            print("  ├── ✅ Local Stdio Server Connected.")

            # 2. Nest Remote HTTP SSE Server Connection Pipeline inside the same lifecycle
            async with sse_client(url=remote_sse_url, headers=sse_headers) as (sse_read, sse_write):
                async with ClientSession(sse_read, sse_write) as sse_session:
                    await sse_session.initialize()
                    
                    sse_toolkit = MCPToolkit(session=sse_session)
                    await sse_toolkit.initialize()
                    file_generation_tools = sse_toolkit.get_tools()
                    print("  └── ✅ Remote HTTP SSE OAuth Server Connected.")

                    # Combine tool inventories into a comprehensive bundle for LangGraph execution
                    unified_mcp_tools = database_tools + file_generation_tools
                    print(f"\n🚀 Total inventory aggregated successfully! {len(unified_mcp_tools)} tools active.")

                    # Compile the dynamic workflow graph using the complete combined tools list
                    graph = create_graph(unified_mcp_tools)
                    
                    config = {
                        "configurable": {
                            "thread_id": session_id,
                            "mcp_tools": unified_mcp_tools 
                        }
                    }

                    print(f"\nConnected to schema: subgroup_{subgroup_id}. Type 'exit' to quit.\n")
                    
                    while True:
                        user_input = input("User: ").strip()
                        if not user_input:
                            continue
                        if user_input.lower() == "exit":
                            break
                            
                        print("\nAssistant: ", end="", flush=True)
                        
                        async for event in graph.astream_events(
                            {
                                "messages": [HumanMessage(content=user_input)], 
                                "subgroup_id": subgroup_id
                            },
                            config=config,
                            version="v2"
                        ):
                            kind = event["event"]
                            
                            # Start loading spinner depending on which tool is triggered
                            if kind == "on_tool_start":
                                tool_name = event["name"]
                                msg = "Fetching data from Trino Database... Please wait"
                                if tool_name in ["save_to_markdown", "generate_multi_format_report"]:
                                    msg = "Generating requested business report asset..."
                                
                                if spinner_task and not spinner_task.done():
                                    spinner_task.cancel()
                                
                                spinner_task = asyncio.create_task(spin_loading(msg))
                            
                            # Clean up active loaders upon finishing execution steps
                            elif kind == "on_tool_end":
                                if spinner_task and not spinner_task.done():
                                    spinner_task.cancel()
                                    await asyncio.sleep(0.05)
                                print("✅ Done.", flush=True)

                            # Stream output characters to shell window in real-time
                            elif kind == "on_chat_model_stream":
                                content = event["data"]["chunk"].content
                                if content:
                                    print(content, end="", flush=True)

                            # Performance logs calculations
                            elif kind == "on_chat_model_end":
                                try:
                                    output_data = event["data"].get("output", {})
                                    usage = getattr(output_data, "usage_metadata", None)
                                    
                                    if usage:
                                        input_tokens = usage.get("input_tokens", 0)
                                        output_tokens = usage.get("output_tokens", 0)
                                        total_tokens = usage.get("total_tokens", 0)
                                        
                                        input_details = usage.get("input_token_details", {})
                                        cache_tokens = input_details.get("cache_read", input_details.get("cached", 0)) if input_details else 0
                                        fresh_input_tokens = input_tokens - cache_tokens
                                        
                                        cost_fresh = fresh_input_tokens * fresh_rate
                                        cost_cached = cache_tokens * cached_rate
                                        cost_output = output_tokens * output_rate
                                        total_cost = cost_fresh + cost_cached + cost_output
                                        
                                        print("\n==========================================================")
                                        print("🎛️ TOKENS USAGE REPORT")
                                        print(f"🔹 Total Context  : {input_tokens} [Fresh: {fresh_input_tokens} | Cached: {cache_tokens} ⚡]")
                                        print(f"🔹 Model Outputs  : {output_tokens} | Total Transacted: {total_tokens}")
                                        print(f"💵 Step Price     : ${total_cost:.6f}")
                                        print("==========================================================\n")
                                except Exception:
                                    pass    
                            
                        print("\n")

def run():
    asyncio.run(run_chat())

if __name__ == "__main__":
    run()




#========================================================================






