from langchain_core.tools import tool
import pandas as pd
import trino
import os

# Leave your get_trino_connection() as is...
# -------------------------
# Trino Connection
# -------------------------
def get_trino_connection():

    return trino.dbapi.connect(
        host=os.getenv("TRINO_HOST"),
        port=int(os.getenv("TRINO_PORT", 443)),
        user=os.getenv("TRINO_USER"),
        http_scheme="https"
    )

@tool
def ask_database(query: str) -> str:
    """
    Executes a pure Trino SQL query string against the database and returns the result.
    Use this to inspect information_schema tables or retrieve analytical metrics.
    Do NOT include trailing semicolons or markdown code blocks in the query argument.
    """
    print("\n\nSQL tool called")
    print(f"SQL Query used:\n{query}")
    conn = get_trino_connection()
    cursor = conn.cursor()
    clean_query = query.strip().rstrip(';')
    try:
        cursor.execute(clean_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        
        # Ekdum clean aur direct output
        return df.to_markdown(index=False)
    except Exception as e:
        return f"Database Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()




















































# @tool
# def ask_database(query: str) -> str:
#     """
#     Executes a pure Trino SQL query string against the database and returns the result.
#     Use this to inspect information_schema tables or retrieve analytical metrics.
#     Do NOT include trailing semicolons or markdown code blocks in the query argument.
#     """
#     conn = get_trino_connection()
#     cursor = conn.cursor()
#     clean_query = query.strip().rstrip(';')
#     try:
#         cursor.execute(clean_query)
#         rows = cursor.fetchall()
#         columns = [desc[0] for desc in cursor.description]
#         df = pd.DataFrame(rows, columns=columns)
        
#         # if len(df) > 30:
#         #     return df.head(30).to_markdown(index=False) + f"\n\n(Truncated {len(df)-30} rows)"
        
#         return df.to_markdown(index=False)
#     except Exception as e:
#         return f"Database Error: {str(e)}"
#     finally:
#         cursor.close()
#         conn.close()
    

# tools/sql_tool.py ke andar ask_database tool ko aise refine karein:

# @tool
# def ask_database(query: str) -> str:
#     """
#     Executes a pure Trino SQL query string against the database and returns the result.
#     Use this to inspect information_schema tables or retrieve analytical metrics.
#     Do NOT include trailing semicolons or markdown code blocks in the query argument.
#     """
#     conn = get_trino_connection()
#     cursor = conn.cursor()
#     clean_query = query.strip().rstrip(';')
#     try:
#         cursor.execute(clean_query)
#         rows = cursor.fetchall()
#         columns = [desc[0] for desc in cursor.description]
#         df = pd.DataFrame(rows, columns=columns)
        
#         # 🚨 STRICT SIZE GUARDRAIL FOR CONTEXT SAFETY:
#         # 15 rows se zyada data memory mein bhejenge toh tokens fatenge.
#         if len(df) > 15:
#             preview = df.head(15).to_markdown(index=False)
#             return (
#                 f"{preview}\n\n"
#                 f"⚠️ NOTICE: Total rows returned were {len(df)}. "
#                 f"Only the top 15 rows are shown above to prevent memory overflow. "
#                 f"If you need deeper trends, write aggregate summary queries (like top 5 or counts) instead."
#             )
            
#         if df.empty:
#             return "Query executed successfully. Result: 0 rows returned (Empty dataset)."
            
#         return df.to_markdown(index=False)
#     except Exception as e:
#         return f"Database Error: {str(e)}"
#     finally:
#         cursor.close()
#         conn.close()    



