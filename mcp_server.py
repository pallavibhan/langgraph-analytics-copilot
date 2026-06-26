

# import os
# import json
# from fastapi import FastAPI, Request, HTTPException, Depends
# from fastapi.responses import StreamingResponse

# app = FastAPI(title="MCP Analytics Server via SSE HTTP")

# def verify_oauth_token(request: Request):
#     auth_header = request.headers.get("Authorization", "")
#     if not auth_header.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Missing or invalid OAuth Token")
#     token = auth_header.split(" ")[1]
#     if token != "valid_mock_token_123":
#         raise HTTPException(status_code=403, detail="Token forbidden or expired")
#     return token

# @app.get("/sse")
# async def mcp_sse_endpoint(request: Request, token: str = Depends(verify_oauth_token)):
#     async def event_generator():
#         init_payload = {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
#         yield f"data: {json.dumps(init_payload)}\n\n"
        
#         # 🔥 DONO TOOLS KI METADATA LIST LIST STREAM KAR RAHE HAIN
#         tools_meta = {
#             "tools": [
#                 {
#                     "name": "ask_database",
#                     "description": "Run optimized Trino SQL query against the retail analytics database."
#                 },
#                 {
#                     "name": "save_to_markdown",
#                     "description": "Export or save executive markdown automated data reports to local files."
#                 }
#             ]
#         }
#         yield f"data: {json.dumps(tools_meta)}\n\n"
        
#         while True:
#             await asyncio.sleep(10)
#             yield ": ping\n\n"

#     import asyncio
#     return StreamingResponse(event_generator(), media_type="text/event-stream")

# @app.post("/messages")
# async def mcp_messages_endpoint(request: Request):
#     try:
#         body = await request.json()
#         method = body.get("method")
        
#         if method == "tools/call":
#             params = body.get("params", {})
#             tool_name = params.get("name")
#             arguments = params.get("arguments", {})
            
#             # 1️⃣ DB TOOL ROUTING
#             if tool_name == "ask_database":
#                 sql_query = arguments.get("query", "SELECT 1;")
#                 return {
#                     "jsonrpc": "2.0",
#                     "result": [{"type": "text", "text": f"Mock Trino DB Result for: {sql_query}"}],
#                     "id": body.get("id", 1)
#                 }
            
#             # 2️⃣ 🔥 MARKDOWN TOOL ROUTING (Naya Block added)
#             elif tool_name == "save_to_markdown":
#                 filename = arguments.get("filename", "report.md")
#                 content = arguments.get("content", "")
#                 return {
#                     "jsonrpc": "2.0",
#                     "result": [{"type": "text", "text": f"Mock File Successfully Generated and saved at: ./{filename}"}],
#                     "id": body.get("id", 1)
#                 }
                
#         return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)




# import os
# import json
# import pandas as pd
# import trino
# from dotenv import load_dotenv
# load_dotenv()  # Yeh aapke project ki saari Trino keys automatic load kar dega!
# from fastapi import FastAPI, Request, HTTPException, Depends
# from fastapi.responses import StreamingResponse

# app = FastAPI(title="MCP Analytics Server via SSE HTTP")

# # -------------------------------------------------------------------------
# # LIVE TRINO CONNECTION ENGINE (Aapka Asli Logic Server Par Shift Hua)
# # -------------------------------------------------------------------------
# def get_trino_connection():
#     return trino.dbapi.connect(
#         host=os.getenv("TRINO_HOST"),
#         port=int(os.getenv("TRINO_PORT", 443)),
#         user=os.getenv("TRINO_USER"),
#         http_scheme="https"
#     )

# # OAuth Guardrail
# def verify_oauth_token(request: Request):
#     auth_header = request.headers.get("Authorization", "")
#     if not auth_header.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Missing or invalid OAuth Token")
#     token = auth_header.split(" ")[1]
#     if token != "valid_mock_token_123":
#         raise HTTPException(status_code=403, detail="Token forbidden or expired")
#     return token

# @app.get("/sse")
# async def mcp_sse_endpoint(request: Request, token: str = Depends(verify_oauth_token)):
#     async def event_generator():
#         init_payload = {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
#         yield f"data: {json.dumps(init_payload)}\n\n"
        
#         tools_meta = {
#             "tools": [
#                 {"name": "ask_database", "description": "Run pure Trino SQL query against the database."},
#                 {"name": "save_to_markdown", "description": "Saves analytical breakdown into a structured Markdown file."}
#             ]
#         }
#         yield f"data: {json.dumps(tools_meta)}\n\n"
        
#         while True:
#             await asyncio.sleep(10)
#             yield ": ping\n\n"

#     import asyncio
#     return StreamingResponse(event_generator(), media_type="text/event-stream")

# @app.post("/messages")
# async def mcp_messages_endpoint(request: Request):
#     try:
#         body = await request.json()
#         if body.get("method") == "tools/call":
#             params = body.get("params", {})
#             tool_name = params.get("name")
#             arguments = params.get("arguments", {})
            
#             # 🗄️ 1. ASLI DATABASE TOOL EXECUTION
#             if tool_name == "ask_database":
#                 query = arguments.get("query")
#                 conn = get_trino_connection()
#                 cursor = conn.cursor()
#                 clean_query = query.strip().rstrip(';')
#                 try:
#                     cursor.execute(clean_query)
#                     rows = cursor.fetchall()
#                     columns = [desc[0] for desc in cursor.description]
#                     df = pd.DataFrame(rows, columns=columns)
#                     result_markdown = df.to_markdown(index=False)
                    
#                     return {
#                         "jsonrpc": "2.0",
#                         "result": [{"type": "text", "text": result_markdown}],
#                         "id": body.get("id", 1)
#                     }
#                 except Exception as db_err:
#                     return {"jsonrpc": "2.0", "result": [{"type": "text", "text": f"Database Error: {str(db_err)}"}], "id": body.get("id", 1)}
#                 finally:
#                     cursor.close()
#                     conn.close()
            
#             # 📄 2. ASLI MARKDOWN FILE WRITING LOGIC
#             elif tool_name == "save_to_markdown":
#                 filename = arguments.get("filename")
#                 content = arguments.get("content")
#                 try:
#                     os.makedirs("outputs", exist_ok=True)
#                     if not filename.endswith(".md"):
#                         filename = f"{filename}.md"
#                     filepath = os.path.join("outputs", filename)
                    
#                     with open(filepath, "w", encoding="utf-8") as f:
#                         f.write(content)
                        
#                     return {
#                         "jsonrpc": "2.0",
#                         "result": [{"type": "text", "text": f"Success: Final report safely exported to Markdown file at '{filepath}'."}],
#                         "id": body.get("id", 1)
#                     }
#                 except Exception as file_err:
#                     return {"jsonrpc": "2.0", "result": [{"type": "text", "text": f"Error saving file: {str(file_err)}"}], "id": body.get("id", 1)}
                    
#         return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


#---------------------------------------------------------------------------------------------------------------
# import os
# import sys
# import pandas as pd
# import trino
# from dotenv import load_dotenv
# from mcp.server.fastmcp import FastMCP

# # .env file se configurations load karne ke liye
# load_dotenv()

# # FastMCP instance initialize karein strictly stdio transport support ke sath
# mcp = FastMCP("Analytics Copilot Server")

# # ---------------------------------------------------------
# # Trino Connection Helper
# # ---------------------------------------------------------
# def get_trino_connection():
#     return trino.dbapi.connect(
#         host=os.getenv("TRINO_HOST"),
#         port=int(os.getenv("TRINO_PORT", 443)),
#         user=os.getenv("TRINO_USER"),
#         http_scheme="https"
#     )

# # ---------------------------------------------------------
# # Tool 1: Ask Database (SQL Tool)
# # ---------------------------------------------------------
# @mcp.tool()
# def ask_database(query: str) -> str:
#     """
#     Executes a pure Trino SQL query string against the database and returns the result in Markdown table format.
#     Do NOT include trailing semicolons or markdown code blocks in the query argument.
#     """
#     # sys.stderr use kar rahe hain taaki stdio protocol channel break na ho
#     print(f"\n[MCP SERVER LOG] Executing SQL Query:\n{query}", file=sys.stderr)
    
#     conn = get_trino_connection()
#     cursor = conn.cursor()
#     clean_query = query.strip().rstrip(';')
#     try:
#         cursor.execute(clean_query)
#         rows = cursor.fetchall()
#         columns = [desc[0] for desc in cursor.description]
#         df = pd.DataFrame(rows, columns=columns)
        
#         # STRICT SIZE GUARDRAIL FOR CONTEXT SAFETY (Max 15 rows)
#         # if len(df) > 15:
#         #     preview = df.head(15).to_markdown(index=False)
#         #     return (
#         #         f"{preview}\n\n"
#         #         f"⚠️ NOTICE: Total rows returned were {len(df)}. "
#         #         f"Only the top 15 rows are shown above to prevent memory overflow."
#         #     )
            
#         if df.empty:
#             return "Query executed successfully. Result: 0 rows returned (Empty dataset)."
            
#         return df.to_markdown(index=False)
#     except Exception as e:
#         return f"Database Error: {str(e)}"
#     finally:
#         cursor.close()
#         conn.close()

# # ---------------------------------------------------------
# # Tool 2: Save To Markdown (File Tool)
# # ---------------------------------------------------------
# @mcp.tool()
# def save_to_markdown(filename: str, content: str) -> str:
#     """
#     Saves the final data metrics, analytical breakdown, and SQL queries into a structured Markdown (.md) file inside the 'outputs' directory.
#     """
#     print(f"\n[MCP SERVER LOG] Exporting file: {filename}", file=sys.stderr)
#     try:
#         # Ensure outputs directory exists
#         os.makedirs("outputs", exist_ok=True)
        
#         # Clean the filename to ensure it ends with .md
#         if not filename.endswith(".md"):
#             filename = f"{filename}.md"
            
#         filepath = os.path.join("outputs", filename)
        
#         with open(filepath, "w", encoding="utf-8") as f:
#             f.write(content)
            
#         return f"Success: Final report safely exported to Markdown file at '{filepath}'."
#     except Exception as e:
#         return f"Error saving file: {str(e)}"

# # Standard execution flow execution configuration
# if __name__ == "__main__":
#     # transport='stdio' rakhna compulsory hai taaki python sub-processes smoothly link ho sakein
#     mcp.run(transport='stdio')


#----------------------------------------------------------------------------------------------------    




import os
import sys
import json
import pandas as pd
import trino
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# .env file se configurations load karne ke liye
load_dotenv()

# FastMCP instance initialize karein strictly stdio transport support ke sath
mcp = FastMCP("Analytics Copilot Server")

# -------------------------------------------------------------------------
# Trino Connection Helper
# -------------------------------------------------------------------------
def get_trino_connection():
    # .env variables ko verify karke connect karte hain
    host = os.getenv("TRINO_HOST")
    port = os.getenv("TRINO_PORT", "443")
    user = os.getenv("TRINO_USER", "admin")
    
    # CRITICAL: Yahan logs sirf stderr par hi hone chahiye taaki protocol transport break na ho
    print(f"[MCP DB SERVER LOG] Connecting to Trino Host: {host} on Port: {port} as User: {user}", file=sys.stderr)
    
    return trino.dbapi.connect(
        host=host,
        port=int(port),
        user=user,
        http_scheme="https"
    )

# -------------------------------------------------------------------------
# Tool 1: Ask Database (SQL Tool)
# -------------------------------------------------------------------------
@mcp.tool(
    name="ask_database",
    description="Executes a pure Trino SQL query string against the analytics database and returns the result in Markdown table format. Do NOT include trailing semicolons or markdown code blocks in the query argument."
)
def ask_database(query: str) -> str:
    # Logger using sys.stderr to safe guard JSON-RPC stdout pipe
    print(f"\n[MCP DB SERVER LOG] Received SQL Query Execution Request:\n{query}", file=sys.stderr)
    
    try:
        conn = get_trino_connection()
        cursor = conn.cursor()
        
        # Semicolon clear pipeline format guardrail
        clean_query = query.strip().rstrip(';')
        cursor.execute(clean_query)
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        
        # # STRICT SIZE GUARDRAIL FOR CONTEXT WINDOW SAFETY
        # if len(df) > 15:
        #     preview = df.head(15).to_markdown(index=False)
        #     print(f"[MCP DB SERVER LOG] Data size warning: Total {len(df)} rows. Truncating to 15.", file=sys.stderr)
        #     return (
        #         f"{preview}\n\n"
        #         f"⚠️ NOTICE: Total rows returned were {len(df)}. "
        #         f"Only the top 15 rows are shown above to prevent token context overflow."
        #     )
            
        if df.empty:
            return "Query executed successfully. Result: 0 rows returned (Empty dataset)."
            
        return df.to_markdown(index=False)
        
    except Exception as db_err:
        error_msg = f"Database Execution Error: {str(db_err)}"
        print(f"[MCP DB SERVER LOG] ERROR: {error_msg}", file=sys.stderr)
        return error_msg
        
    finally:
        try:
            cursor.close()
            conn.close()
            print("[MCP DB SERVER LOG] Connections safely closed.", file=sys.stderr)
        except NameError:
            pass  # Variable initialize nahi hui thi agar pehle hi step par crash hua

# Standard execution flow execution configuration for Stdio Protocol
if __name__ == "__main__":
    # CRITICAL: Stdio protocol ko run karne ke liye default transport='stdio' hona compulsory hai
    mcp.run(transport='stdio')