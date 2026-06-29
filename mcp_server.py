
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