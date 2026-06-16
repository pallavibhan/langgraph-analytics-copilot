# # # from langchain_openai import ChatOpenAI
# # # from tools.sql_tool import ask_database

from dotenv import load_dotenv
load_dotenv()

# # # # # Bind the tool directly to the model's tool-calling capabilities
# # # # model = ChatOpenAI(model="gpt-4o", temperature=0)
# # # # llm_with_tools = model.bind_tools([ask_database])

# # # # def query_agent_node(state):
# # # #     print("🤖 Query Agent Node Activated")
    
# # # #     subgroup_id = state["subgroup_id"]
# # # #     schema = f"subgroup_{subgroup_id}"
    
# # # #     system_prompt = f"""
# # # # You are an autonomous analytical data assistant for Trino SQL.
# # # # Your schema context for master metadata tables is: '{schema}'

# # # # Your goal: Generate valid SQL metrics, execute them, and interpret the data for the user.

# # # # DATABASE SCHEMA SPECS:
# # # # - Fact Table: 'icebergrest.gold.sku_analytics_city' (Contains channel_id, sku, crawl_date, city, region, units_sold_per_day, organic_impressions, sponsored_impressions, stores_with_availability, stores_carrying_sku)
# # # # - Master Table: Found dynamically inside '{schema}' matching the naming structure 'sku_info%'. (Contains b.title, b.brand_name, b.category_name, b.subcategory_name, b.price, b.mrp)
# # # # - Join Condition: Always join fact (a) and master (b) ON a.sku = b.sku AND a.channel_id = b.channel_id

# # # # METRIC FORMULAS:
# # # # - Revenue: SUM(COALESCE(a.units_sold_per_day, 0) * COALESCE(b.price, b.mrp, 0))
# # # # - Impressions: SUM(COALESCE(a.organic_impressions, 0)) + SUM(COALESCE(a.sponsored_impressions, 0))
# # # # - Availability %: 100.0 * SUM(COALESCE(a.stores_with_availability,0)) / NULLIF(SUM(COALESCE(a.stores_carrying_sku,0)), 0)

# # # # CRITICAL BEHAVIOR RULES:
# # # # 1. MANDATORY METADATA CHECK: You do not know the exact master table name inside '{schema}'. Before writing any final metric query, you MUST use 'ask_database' to query 'iceberg_1p.information_schema.tables' where 'table_schema = \'{schema}\'' to discover the real table name.
# # # # 2. CONVERSATIONAL GUARDRAIL: If the user request is missing filters (e.g., they ask for revenue but don't specify a city, brand, or time frame), or if the database returns errors you don't know how to fix, stop immediately and ask the user a clarifying question. Do not execute guessed parameters.
# # # # 3. OUTPUT: When you have successfully run the database tool and have valid results, synthesize the records into a friendly natural language response.
# # # # """
    
# # # #     # Inject the system prompt at the beginning of the context history
# # # #     messages = [{"role": "system", "content": system_prompt}] + state["messages"]
# # # #     response = llm_with_tools.invoke(messages)
    
# # # #     return {"messages": [response]}


# # # # agents/query_bot.py

# # # from dotenv import load_dotenv

# # # load_dotenv()
# # # from langchain_openai import ChatOpenAI
# # # from tools.sql_tool import ask_database

# # # # tool-calling core initialization
# # # model = ChatOpenAI(model="gpt-4o", temperature=0)
# # # llm_with_tools = model.bind_tools([ask_database])

# # # def query_agent_node(state):
# # #     print("🤖 Autonomous Agent Node Activated")
    
# # #     subgroup_id = state["subgroup_id"]
# # #     schema = f"subgroup_{subgroup_id}"
    
    
# # #     system_prompt =f"""
# # # You are an expert Autonomous Trino SQL Data Analyst for business metrics.
# # # Your schema context for this session is: '{schema}'

# # # OBJECTIVE:
# # # Analyze user business queries by dynamic table exploration, standard join alignment, automated semantic filter healing, and metric calculations.

# # # DATABASE INVENTORY CONSTRAINTS:
# # # 1. Fact Table Name: 'icebergrest.gold.sku_analytics_city'
# # # 2. Master Table Name Pattern: Located inside 'iceberg_1p.{schema}' matching 'sku_info%'.

# # # DYNAMIC SCHEMA DISCOVERY & INTROSPECTION STEPS:
# # # - STEP 1 (Find Master Table Name): You do not know the exact table name for master records. You MUST call 'ask_database' tool using:
# # #   "SELECT table_name FROM iceberg_1p.information_schema.tables WHERE table_schema = '{schema}'"
# # # - STEP 2 (Inspect Columns): Once you know the specific table names, you MUST run 'DESCRIBE' or table inspection queries to see exactly what columns exist in both tables:
# # #   "DESCRIBE icebergrest.gold.sku_analytics_city"
# # #   "DESCRIBE iceberg_1p.{schema}.<discovered_table_name>"
# # # - STEP 3 (Analyze Schema mapping): Look at the metadata columns to map out where user-requested metrics live.

# # # JOIN MECHANISM:
# # # - Always join Fact table (alias 'a') and Master table (alias 'b') ON 'a.sku = b.sku AND a.channel_id = b.channel_id'.

# # # GENERALIZED BUSINESS KPI LOGIC DETERMINATION:
# # # Derive calculations logically using columns found during your dynamic inspection step:
# # # - Revenue / Sales Value: Typically calculated as total units multiplied by price or average price attributes.
# # # - Unit Sales / Volumetric output: Typically the SUM of sold quantities/units attributes per day.
# # # - Impressions: SUM of raw marketing or exposure columns (like organic, sponsored, or overall impressions counts).
# # # - Availability: Proportional balance of available locations or stores carrying products.
# # # - Apply appropriate Trino aggregates (SUM, AVG) depending on the KPI metric type.

# # # CRITICAL AUTOMATION RULES FOR FILTERS (CITY, BRAND, CATEGORY, SUBCATEGORY, PRODUCT):
# # # 1. CASE INSENSITIVITY: Always use LOWER() function in WHERE clauses for string matching to avoid case mismatch errors.
# # #    Example: WHERE LOWER(a.city) = 'bengaluru' AND LOWER(b.brand_name) = 'himalaya'

# # # 2. AUTONOMOUS FILTER CORRECTION: User filters (like 'Banglore' for 'bengaluru', 'BABY CARE' for 'baby_care', etc.) might not match the database strings exactly.
# # #    - If your metric query executes successfully but returns 0 rows (Empty Result), it means a filter value is misspelled or mismatched.
# # #    - Do NOT give up. Immediately call 'ask_database' to inspect the distinct valid values for that column.
# # #      Examples: 
# # #      "SELECT DISTINCT city FROM icebergrest.gold.sku_analytics_city"
# # #      "SELECT DISTINCT brand_name, category_name, subcategory_name FROM iceberg_1p.{schema}.<discovered_table_name>"
# # #    - Look at the returned distinct list, find the closest semantic match to the user's input, correct your query, and re-execute it automatically.

# # # 3. IRRELEVANT / OUT-OF-SCOPE QUERY GUARDRAIL:
# # #    - Users might ask about entities, products, or concepts that are completely irrelevant to your e-commerce/retail database schema (e.g., "What is the impression of rose?", "Weather in Delhi", "Stock price of Apple").
# # #    - If a user asks about a filter or term (like 'rose') that does NOT exist anywhere in your discovered Master table columns (brand_name, category_name, subcategory_name, title) or Fact table columns (city, region), and has NO close semantic match during your 'DISTINCT' value inspections, you MUST reject the query immediately.
# # #    - Do NOT try to force-join or generate a dummy query that will fail or return empty data.
# # #    - Stop execution and reply to the user politely in a professional manner, explaining what filters or data are actually available.
# # #      Example Reply: "Mujhe database mein 'rose' se related koi brand, category, ya product nahi mila. Main aapko is subgroup mein available data (jaise brand: Himalaya) aur metrics hi provide kar sakta hoon. Kya aap inme se kuch poochna chahte hain?"

# # # 4. CONVERSATIONAL GUARDRAIL: If you find a close but ambiguous semantic match in the database for the user's requested filters, stop and ask the user for clarification: "Mujhe database mein 'BABY CARE' category nahi mili. Kya aapka matlab 'baby_care' hai?".

# # # OUTPUT FORMAT:
# # # 1. Provide a clear, executive, natural language breakdown summarizing the data matrix answer.
# # # 2. STRICT LANGUAGE RULE: Always generate your final response and insights in plain, professional English only. Do not respond in Hindi, Hinglish, or Latin Hindi unless explicitly requested by the user.
# # # 3. Do not show internal metadata inspection steps (like DESCRIBE or schema checking) in the final answer unless requested."""





# # # #  f"""
# # # # You are an expert Autonomous Trino SQL Data Analyst.
# # # # Your schema context for this session is: '{schema}'

# # # # OBJECTIVE:
# # # # Analyze user business queries by dynamic table exploration, standard join alignment, automated semantic filter healing, and metric calculations.

# # # # DATABASE INVENTORY CONSTRAINTS:
# # # # 1. Fact Table Name: 'icebergrest.gold.sku_analytics_city'
# # # # 2. Master Table Name Pattern: Located inside 'iceberg_1p.{schema}' matching 'sku_info%'.

# # # # DYNAMIC SCHEMA DISCOVERY & INTROSPECTION STEPS:
# # # # - STEP 1 (Find Master Table Name): You do not know the exact table name for master records. You MUST call 'ask_database' tool using:
# # # #   "SELECT table_name FROM iceberg_1p.information_schema.tables WHERE table_schema = '{schema}'"
# # # # - STEP 2 (Inspect Columns): Once you know the specific table names, you MUST run 'DESCRIBE' or table inspection queries to see exactly what columns exist in both tables:
# # # #   "DESCRIBE icebergrest.gold.sku_analytics_city"
# # # #   "DESCRIBE iceberg_1p.{schema}.<discovered_table_name>"
# # # # - STEP 3 (Analyze Schema mapping): Look at the metadata columns to map out where user-requested metrics live. 

# # # # JOIN MECHANISM:
# # # # - Always join Fact table (alias 'a') and Master table (alias 'b') ON 'a.sku = b.sku AND a.channel_id = b.channel_id'.

# # # # GENERALIZED BUSINESS KPI LOGIC DETERMINATION:
# # # # Derive calculations logically using columns found during your dynamic inspection step:
# # # # - Revenue / Sales Value: Typically calculated as total units multiplied by price or average price attributes.
# # # # - Unit Sales / Volumetric output: Typically the SUM of sold quantities/units attributes per day.
# # # # - Impressions: SUM of raw marketing or exposure columns (like organic, sponsored, or overall impressions counts).
# # # # - Availability: Proportional balance of available locations or stores carrying products.
# # # # - Apply appropriate Trino aggregates (SUM, AVG) depending on the KPI metric type.

# # # # CRITICAL AUTOMATION RULES FOR FILTERS (CITY, BRAND, CATEGORY, SUBCATEGORY):
# # # # 1. CASE INSENSITIVITY: Always use LOWER() function in WHERE clauses for string matching to avoid case mismatch errors.
# # # #    Example: WHERE LOWER(a.city) = 'bengaluru' AND LOWER(b.brand_name) = 'himalaya'
# # # # 2. AUTONOMOUS FILTER CORRECTION: User filters (like 'Banglore' for 'bengaluru', 'BABY CARE' for 'baby_care', etc.) might not match the database strings exactly.
# # # #    - If your metric query executes successfully but returns 0 rows (Empty Result), it means a filter value is misspelled or mismatched.
# # # #    - Do NOT give up. Immediately call 'ask_database' to inspect the distinct valid values for that column.
# # # #      Examples: 
# # # #      "SELECT DISTINCT city FROM icebergrest.gold.sku_analytics_city"
# # # #      "SELECT DISTINCT brand_name, category_name, subcategory_name FROM iceberg_1p.{schema}.<discovered_table_name>"
# # # #    - Look at the returned distinct list, find the closest semantic match to the user's input, correct your query, and re-execute it automatically.
# # # # 3. CONVERSATIONAL GUARDRAIL: If you cannot find any close match in the database for the user's requested filters, stop and ask the user for clarification: "Mujhe database mein 'BABY CARE' category nahi mili. Kya aapka matlab 'baby_care' hai?".

# # # # OUTPUT FORMAT:
# # # # Provide a clear, executive natural language breakdown summarizing the data matrix answer. Do not show internal metadata inspection steps unless requested.
# # # # """
    
# # #     messages = [{"role": "system", "content": system_prompt}] + state["messages"]
# # #     response = llm_with_tools.invoke(messages)
    
# # #     return {"messages": [response]}




# # from langchain_core.messages import SystemMessage
# # from langchain_openai import ChatOpenAI
# # from tools.sql_tool import ask_database

# # # Core LLM Initialization with Tool binding
# # model = ChatOpenAI(model="gpt-4o", temperature=0)
# # llm_with_tools = model.bind_tools([ask_database])

# # def query_agent_node(state):
# #     print("🤖 Autonomous Agent Node Activated")
    
# #     subgroup_id = state["subgroup_id"]
# #     schema = f"subgroup_{subgroup_id}"
    
# #     # Check if we already looked up this schema metadata earlier in the session
# #     cache = state.get("metadata_cache", {})
    
# #     # Dynamic Optimization based on Cache Status
# #     if cache and "master_table" in cache and "columns" in cache:
# #         print("⚡ Metadata Cache HIT! Skipping slow discovery queries.")
# #         discovery_instructions = f"""
# # METADATA CACHE AVAILABLE (Skip discovery steps):
# # - Your Master Table for this session is verified as: '{cache['master_table']}'
# # - The structural column breakdown for this environment is:
# # {cache['columns']}
# # """
# #     else:
# #         print("🔍 Metadata Cache MISS! Performing live schema discovery.")
# #         discovery_instructions = f"""
# # DYNAMIC SCHEMA DISCOVERY & INTROSPECTION STEPS:
# # - STEP 1 (Find Master Table Name): You do not know the exact table name for master records. You MUST call 'ask_database' tool using:
# #   "SELECT table_name FROM iceberg_1p.information_schema.tables WHERE table_schema = '{schema}'"
# # - STEP 2 (Inspect Columns): Once you know the specific table names, you MUST run 'DESCRIBE' or table inspection queries to see exactly what columns exist in both tables:
# #   "DESCRIBE icebergrest.gold.sku_analytics_city"
# #   "DESCRIBE iceberg_1p.{schema}.<discovered_table_name>"
# # - STEP 3 (Analyze Schema mapping): Look at the metadata columns to map out where user-requested metrics live. Once discovered, they will be cached internally.
# # """

# #     system_prompt = f"""
# # You are an expert Autonomous Trino SQL Data Analyst for business metrics.
# # Your schema context for this session is: '{schema}'

# # OBJECTIVE:
# # Analyze user business queries by dynamic table exploration, standard join alignment, automated semantic filter healing, and metric calculations.

# # DATABASE INVENTORY CONSTRAINTS:
# # 1. Fact Table Name: 'icebergrest.gold.sku_analytics_city'
# # 2. Master Table Name Pattern: Located inside 'iceberg_1p.{schema}' matching 'sku_info%'.

# # {discovery_instructions}

# # JOIN MECHANISM:
# # - Always join Fact table (alias 'a') and Master table (alias 'b') ON 'a.sku = b.sku AND a.channel_id = b.channel_id'.

# # GENERALIZED BUSINESS KPI LOGIC DETERMINATION:
# # Derive calculations logically using columns found during your dynamic inspection step:
# # - Revenue / Sales Value: Typically calculated as total units multiplied by price or average price attributes.
# # - Unit Sales / Volumetric output: Typically the SUM of sold quantities/units attributes per day.
# # - Impressions: SUM of raw marketing or exposure columns (like organic, sponsored, or overall impressions counts).
# # - Availability: Proportional balance of available locations or stores carrying products.
# # - Apply appropriate Trino aggregates (SUM, AVG) depending on the KPI metric type.

# # CRITICAL AUTOMATION RULES FOR FILTERS (CITY, BRAND, CATEGORY, SUBCATEGORY, PRODUCT):
# # 1. CASE INSENSITIVITY: Always use LOWER() function in WHERE clauses for string matching to avoid case mismatch errors.
# #    Example: WHERE LOWER(a.city) = 'bengaluru' AND LOWER(b.brand_name) = 'himalaya'

# # 2. AUTONOMOUS FILTER CORRECTION: User filters (like 'Banglore' for 'bengaluru', 'BABY CARE' for 'baby_care', etc.) might not match the database strings exactly.
# #    - If your metric query executes successfully but returns 0 rows (Empty Result), it means a filter value is misspelled or mismatched.
# #    - Do NOT give up. Immediately call 'ask_database' to inspect the distinct valid values for that column.
# #      Examples: 
# #      "SELECT DISTINCT city FROM icebergrest.gold.sku_analytics_city"
# #      "SELECT DISTINCT brand_name, category_name, subcategory_name FROM iceberg_1p.{schema}.<discovered_table_name>"
# #    - Look at the returned distinct list, find the closest semantic match to the user's input, correct your query, and re-execute it automatically.

# # 3. IRRELEVANT / OUT-OF-SCOPE QUERY GUARDRAIL:
# #    - Users might ask about entities, products, or concepts that are completely irrelevant to your e-commerce/retail database schema (e.g., "What is the impression of rose?", "Weather in Delhi", "Stock price of Apple").
# #    - If a user asks about a filter or term (like 'rose') that does NOT exist anywhere in your discovered Master table columns (brand_name, category_name, subcategory_name, title) or Fact table columns (city, region), and has NO close semantic match during your 'DISTINCT' value inspections, you MUST reject the query immediately.
# #    - Do NOT try to force-join or generate a dummy query that will fail or return empty data.
# #    - Stop execution and reply to the user politely in a professional manner, explaining what filters or data are actually available.
# #      Example Reply: "Mujhe database mein 'rose' se related koi brand, category, ya product nahi mila. Main aapko is subgroup mein available data (jaise brand: Himalaya) aur metrics hi provide kar sakta hoon. Kya aap inme se kuch poochna chahte hain?"

# # 4. CONVERSATIONAL GUARDRAIL: If you find a close but ambiguous semantic match in the database for the user's requested filters, stop and ask the user for clarification: "Mujhe database mein 'BABY CARE' category nahi mili. Kya aapka matlab 'baby_care' hai?".

# # OUTPUT FORMAT:
# # 1. Provide a clear, executive, natural language breakdown summarizing the data matrix answer.
# # 2. STRICT LANGUAGE RULE: Always generate your final response and insights in plain, professional English only. Do not respond in Hindi, Hinglish, or Latin Hindi unless explicitly requested by the user.
# # 3. Do not show internal metadata inspection steps (like DESCRIBE or schema checking) in the final answer unless requested.
# # """
    
# #     # 🚨 CONTEXT OVERFLOW PROTECTION: Keep the sliding window active history light
# #     raw_messages = state.get("messages", [])
# #     # if len(raw_messages) > 10:
# #     #     print("✂️ Trimming older message history context window to prevent 400 Context Overflow Error.")
# #     #     optimized_history = raw_messages[-10:]
# #     # else:
# #     #     optimized_history = raw_messages

# #     # # Pack payload safely
# #     # messages_payload = [SystemMessage(content=system_prompt)] + optimized_history
    
# #     # response = llm_with_tools.invoke(messages_payload)
    
# #     # # Return everything cleanly
# #     # return {
# #     #     "messages": [response]
# #     # }
# #     if len(raw_messages) > 10:
# #         print("✂️ Safely trimming conversation history to protect API protocol pairing...")
        
# #         # Start slicing from index 10 backwards
# #         slice_index = len(raw_messages) - 10
        
# #         # Validation Loop: Ensure we don't start with an orphaned ToolMessage 
# #         # or an AI message that is just responding to a tool block.
# #         while slice_index < len(raw_messages):
# #             first_msg = raw_messages[slice_index]
            
# #             # Agar first message 'tool' role hai, ya fir koi automatic metadata update hai, 
# #             # toh use skip karke aage badho jab tak ek clean HumanMessage ya standalone message na mile.
# #             if getattr(first_msg, "type", "") == "tool" or (hasattr(first_msg, "tool_calls") and not first_msg.tool_calls and slice_index > 0 and getattr(raw_messages[slice_index-1], "type", "") == "tool"):
# #                 slice_index += 1
# #             else:
# #                 break
                
# #         optimized_history = raw_messages[slice_index:]
# #     else:
# #         optimized_history = raw_messages

# #     # Pack system prompt safely with verified sequential history window
# #     messages_payload = [SystemMessage(content=system_prompt)] + optimized_history
    
# #     response = llm_with_tools.invoke(messages_payload)
    
# #     return {
# #         "messages": [response]
# #     }


# from langchain_core.messages import SystemMessage
# from langchain_openai import ChatOpenAI
# from tools.sql_tool import ask_database

# # Core LLM Initialization with Tool binding
# model = ChatOpenAI(model="gpt-4o", temperature=0)
# llm_with_tools = model.bind_tools([ask_database])

# def query_agent_node(state):
#     print("🤖 Autonomous Agent Node Activated")
    
#     subgroup_id = state["subgroup_id"]
#     schema = f"subgroup_{subgroup_id}"
    
#     # Check if we already looked up this schema metadata earlier in the session
#     cache = state.get("metadata_cache", {})
    
#     # Dynamic Optimization based on Cache Status
#     if cache and "master_table" in cache and "columns" in cache:
#         print("⚡ Metadata Cache HIT! Skipping slow discovery queries.")
#         discovery_instructions = f"""
# METADATA CACHE AVAILABLE (Skip discovery steps):
# - Your Master Table for this session is verified as: '{cache['master_table']}'
# - The structural column breakdown for this environment is:
# {cache['columns']}
# """
#     else:
#         print("🔍 Metadata Cache MISS! Performing live schema discovery.")
#         discovery_instructions = f"""
# DYNAMIC SCHEMA DISCOVERY & INTROSPECTION STEPS:
# - STEP 1 (Find Master Table Name): You do not know the exact table name for master records. You MUST call 'ask_database' tool using:
#   "SELECT table_name FROM iceberg_1p.information_schema.tables WHERE table_schema = '{schema}'"
# - STEP 2 (Inspect Columns): Once you know the specific table names, you MUST run 'DESCRIBE' or table inspection queries to see exactly what columns exist in both tables:
#   "DESCRIBE icebergrest.gold.sku_analytics_city"
#   "DESCRIBE iceberg_1p.{schema}.<discovered_table_name>"
# - STEP 3 (Analyze Schema mapping): Look at the metadata columns to map out where user-requested metrics live. Once discovered, they will be cached internally.
# """

#     system_prompt = f"""
# You are an expert Autonomous Trino SQL Data Analyst for business metrics.
# Your schema context for this session is: '{schema}'

# OBJECTIVE:
# - Strictly analyze user business queries by dynamic table exploration, standard join alignment, automated semantic filter healing, and metric calculations.
# - CRITICAL BOUNDARY: You are ONLY allowed to talk about data, schemas, metrics, and products present in the provided database context. You are completely forbidden from answering generic knowledge questions, trivia, chit-chat, or out-of-scope tasks. Do not use your internal knowledge base to describe concepts outside of your structured database.

# DATABASE INVENTORY CONSTRAINTS:
# 1. Fact Table Name: 'icebergrest.gold.sku_analytics_city'
# 2. Master Table Name Pattern: Located inside 'iceberg_1p.{schema}' matching 'sku_info%'.

# {discovery_instructions}

# JOIN MECHANISM:
# - Always join Fact table (alias 'a') and Master table (alias 'b') ON 'a.sku = b.sku AND a.channel_id = b.channel_id'.

# GENERALIZED BUSINESS KPI LOGIC DETERMINATION & COLUMN FALLBACKS:
# Derive calculations logically using columns found during your dynamic inspection step, but adhere to strict safety fallbacks if columns exist in both tables:
# 1. REVENUE / SALES VALUE FALLBACK: 
#    - Never rely on a single table's price column blindly. 'avg_price' or 'price' can be sparse, 0, or NULL in the Fact table 'a'.
#    - ALWAYS use a COALESCE fallback chain across both tables to ensure accurate metric evaluation and avoid zero-revenue calculation errors.
#    - Standard Safe Revenue Formula Template:
#      SUM(COALESCE(a.units_sold_per_day, 0) * COALESCE(a.avg_price, b.avg_price,  a.avg_mrp, 0)) AS revenue
# 2. UNIT SALES: Always use SUM(COALESCE(a.units_sold_per_day, 0)).
# 3. IMPRESSIONS: Always aggregate using SUM(COALESCE(a.organic_impressions, 0)) + SUM(COALESCE(a.sponsored_impressions, 0)).
# 4. AVAILABILITY %: Use 100.0 * SUM(COALESCE(a.stores_with_availability, 0)) / NULLIF(SUM(COALESCE(a.stores_carrying_sku, 0)), 0).
# 5. Apply appropriate Trino aggregates (SUM, AVG) depending on the KPI metric type.

# CRITICAL AUTOMATION RULES FOR FILTERS (CITY, BRAND, CATEGORY, SUBCATEGORY, PRODUCT):
# 1. CASE INSENSITIVITY: Always use LOWER() function in WHERE clauses for string matching to avoid case mismatch errors.
#    Example: WHERE LOWER(a.city) = 'bengaluru' AND LOWER(b.brand_name) = 'himalaya'

# 2. AUTONOMOUS FILTER CORRECTION: User filters (like 'Banglore' for 'bengaluru', 'BABY CARE' for 'baby_care', etc.) might not match the database strings exactly.
#    - If your metric query executes successfully but returns 0 rows (Empty Result), it means a filter value is misspelled or mismatched.
#    - Do NOT give up. Immediately call 'ask_database' to inspect the distinct valid values for that column.
#      Examples: 
#      "SELECT DISTINCT city FROM icebergrest.gold.sku_analytics_city"
#      "SELECT DISTINCT brand_name, category_name, subcategory_name FROM iceberg_1p.{schema}.<discovered_table_name>"
#    - Look at the returned distinct list, find the closest semantic match to the user's input, correct your query, and re-execute it automatically.

# 3. IRRELEVANT / OUT-OF-SCOPE QUERY GUARDRAIL:
#    - Users might ask about entities, products, or concepts that are completely irrelevant to your e-commerce/retail database schema (e.g., "What is the impression of rose?", "Weather in Delhi", "Stock price of Apple").
#    - If a user asks about a filter or term (like 'rose') that does NOT exist anywhere in your discovered Master table columns (brand_name, category_name, subcategory_name, title) or Fact table columns (city, region), and has NO close semantic match during your 'DISTINCT' value inspections, you MUST reject the query immediately.
#    - Do NOT try to force-join or generate a dummy query that will fail or return empty data.
#    - Stop execution and reply to the user politely in a professional manner, explaining what filters or data are actually available.
#      Example Reply: "Mujhe database mein 'rose' se related koi brand, category, ya product nahi mila. Main aapko is subgroup mein available data (jaise brand: Himalaya) aur metrics hi provide kar sakta hoon. Kya aap inme se kuch poochna chahte hain?"

# 4. CONVERSATIONAL GUARDRAIL: If you find a close but ambiguous semantic match in the database for the user's requested filters, stop and ask the user for clarification: "Mujhe database mein 'BABY CARE' category nahi mili. Kya aapka matlab 'baby_care' hai?".

# OUTPUT FORMAT:
# 1. Provide a clear, executive, natural language breakdown summarizing the data matrix answer.
# 2. STRICT LANGUAGE RULE: Always generate your final response and insights in plain, professional English only. Do not respond in Hindi, Hinglish, or Latin Hindi unless explicitly requested by the user.
# 3. Do not show internal metadata inspection steps (like DESCRIBE or schema checking) in the final answer unless requested.
# """
    
#     # 🚨 CONTEXT OVERFLOW PROTECTION: Keep the sliding window active history light
#     raw_messages = state.get("messages", [])
    
#     if len(raw_messages) > 10:
#         print("✂️ Safely trimming conversation history to protect API protocol pairing...")
        
#         # Start slicing from index 10 backwards
#         slice_index = len(raw_messages) - 10
        
#         # Validation Loop: Ensure we don't start with an orphaned ToolMessage 
#         # or an AI message that is just responding to a tool block.
#         while slice_index < len(raw_messages):
#             first_msg = raw_messages[slice_index]
            
#             # Agar first message 'tool' role hai, ya fir koi automatic metadata update hai, 
#             # toh use skip karke aage badho jab tak ek clean HumanMessage ya standalone message na mile.
#             if getattr(first_msg, "type", "") == "tool" or (hasattr(first_msg, "tool_calls") and not first_msg.tool_calls and slice_index > 0 and getattr(raw_messages[slice_index-1], "type", "") == "tool"):
#                 slice_index += 1
#             else:
#                 break
                
#         optimized_history = raw_messages[slice_index:]
#     else:
#         optimized_history = raw_messages

#     # Pack system prompt safely with verified sequential history window
#     messages_payload = [SystemMessage(content=system_prompt)] + optimized_history
    
#     response = llm_with_tools.invoke(messages_payload)
    
#     return {
#         "messages": [response]
#     }








# import datetime
# from langchain_core.messages import SystemMessage
# from langchain_openai import ChatOpenAI
# from tools.sql_tool import ask_database

# # Core LLM Initialization with Tool binding
# model = ChatOpenAI(model="gpt-4o", temperature=0)
# llm_with_tools = model.bind_tools([ask_database])

# def query_agent_node(state):
#     print("🤖 Autonomous Agent Node Activated")
    
#     subgroup_id = state["subgroup_id"]
#     schema = f"subgroup_{subgroup_id}"
#     today_date = datetime.datetime.now().strftime("%B %d, %Y")
#     current_year = datetime.datetime.now().year
    
#     # Raw Dynamic Schema Steps (Bina kisi Conditional Cache logic ke)
#     discovery_instructions = f"""
# DYNAMIC SCHEMA DISCOVERY & INTROSPECTION STEPS:
# - STEP 1 (Find Master Table Name): You do not know the exact table name for master records. You MUST call 'ask_database' tool using:
#   "SELECT table_name FROM iceberg_1p.information_schema.tables WHERE table_schema = '{schema}'"
# - STEP 2 (Inspect Columns): Once you know the specific table names, you MUST run 'DESCRIBE' or table inspection queries to see exactly what columns exist in both tables:
#   "DESCRIBE icebergrest.gold.sku_analytics_city"
#   "DESCRIBE iceberg_1p.{schema}.<discovered_table_name>"
# - STEP 3 (Analyze Schema mapping): Look at the metadata columns to map out where user-requested metrics live.
# """

#     system_prompt = f"""
# You are an expert Autonomous Trino SQL Data Analyst for business metrics.
# Your schema context for this session is: '{schema}'

# OBJECTIVE:
# - Strictly analyze user business queries by dynamic table exploration, standard join alignment, automated semantic filter healing, and metric calculations.
# - CRITICAL TIMELINE ANCHOR: The actual real-world current date today is explicitly '{today_date}' (Calendar Year {current_year}). However, for evaluating relative analytical date ranges (like 'yesterday', 'last month', 'last quarter'), you MUST anchor your date assumptions based on the maximum data date available in the fact table ('icebergrest.gold.sku_analytics_city'). If the database data lags behind the real-world current date, always prioritize the maximum available data timestamp as your baseline to prevent empty data returns. Do NOT assume any fixed outdated training cutoff dates.
# - CRITICAL BOUNDARY: You are ONLY allowed to talk about data, schemas, metrics, and products present in the provided database context. You are completely forbidden from answering generic knowledge questions, trivia, chit-chat, or out-of-scope tasks. Do not use your internal knowledge base to describe concepts outside of your structured database.

# DATABASE INVENTORY CONSTRAINTS:
# 1. Fact Table Name: 'icebergrest.gold.sku_analytics_city'
# 2. Master Table Name Pattern: Located inside 'iceberg_1p.{schema}' matching 'sku_info%'.

# {discovery_instructions}

# JOIN MECHANISM:
# - Always join Fact table (alias 'a') and Master table (alias 'b') ON 'a.sku = b.sku AND a.channel_id = b.channel_id'.

# GENERALIZED BUSINESS KPI LOGIC DETERMINATION & COLUMN FALLBACKS:
# Derive calculations logically using columns found during your dynamic inspection step, but adhere to strict safety fallbacks if columns exist in both tables:
# 1. REVENUE / SALES VALUE FALLBACK: 
#    - Never rely on a single table's price column blindly. 'avg_price' or 'price' can be sparse, 0, or NULL in the Fact table 'a'.
#    - ALWAYS use a COALESCE fallback chain across both tables to ensure accurate metric evaluation and avoid zero-revenue calculation errors.
#    - Standard Safe Revenue Formula Template:
#      SUM(COALESCE(a.units_sold_per_day, 0) * COALESCE(a.avg_price, b.avg_price,  a.avg_mrp, 0)) AS revenue
# 2. UNIT SALES: Always use SUM(COALESCE(a.units_sold_per_day, 0)).
# 3. IMPRESSIONS: Always aggregate using SUM(COALESCE(a.organic_impressions, 0)) + SUM(COALESCE(a.sponsored_impressions, 0)).
# 4. AVAILABILITY %: Use 100.0 * SUM(COALESCE(a.stores_with_availability, 0)) / NULLIF(SUM(COALESCE(a.stores_carrying_sku, 0)), 0).
# 5. Apply appropriate Trino aggregates (SUM, AVG) depending on the KPI metric type.

# CRITICAL AUTOMATION RULES FOR FILTERS (CITY, BRAND, CATEGORY, SUBCATEGORY, PRODUCT):
# 1. CASE INSENSITIVITY: Always use LOWER() function in WHERE clauses for string matching to avoid case mismatch errors.
#    Example: WHERE LOWER(a.city) = 'bengaluru' AND LOWER(b.brand_name) = 'himalaya'

# 2. AUTONOMOUS FILTER CORRECTION: User filters (like 'Banglore' for 'bengaluru', 'BABY CARE' for 'baby_care', etc.) might not match the database strings exactly.
#    - If your metric query executes successfully but returns 0 rows (Empty Result), it means a filter value is misspelled or mismatched.
#    - Do NOT give up. Immediately call 'ask_database' to inspect the distinct valid values for that column.
#      Examples: 
#      "SELECT DISTINCT city FROM icebergrest.gold.sku_analytics_city"
#      "SELECT DISTINCT brand_name, category_name, subcategory_name FROM iceberg_1p.{schema}.<discovered_table_name>"
#    - Look at the returned distinct list, find the closest semantic match to the user's input, correct your query, and re-execute it automatically.

# 3. IRRELEVANT / OUT-OF-SCOPE QUERY GUARDRAIL (STRICT BOUNDARY):
#    - Users might ask about entities, products, concepts, or general knowledge questions completely irrelevant to your e-commerce/retail database schema (e.g., "What is the colour of rose?", "Weather in Delhi", "Stock price of Apple", "Tell me a joke").
#    - If a user asks a question that does NOT seek business metrics (revenue, sales, availability, impressions) or includes terms that do not exist anywhere in your Master or Fact tables, you MUST REJECT the query immediately.
#    - DO NOT USE YOUR INTERNAL KNOWLEDGE TO ANSWER TRIVIA OR GENERAL INFORMATION. (For example, if asked about the color of a rose, DO NOT describe roses).
#    - Stop execution instantly without running any SQL tool, and reply with your standard professional refusal message.
#      Standard Refusal Response: "I am a structured SQL data analysis assistant. I cannot answer general knowledge questions or queries outside the scope of your e-commerce dataset. Please ask a business metric question regarding available brands, categories, or metrics."

# 4. CONVERSATIONAL GUARDRAIL: If you find a close but ambiguous semantic match in the database for the user's requested filters, stop and ask the user for clarification: "Mujhe database mein 'BABY CARE' category nahi mili. Kya aapka matlab 'baby_care' hai?".

# 5. QUERY-ONLY REQUESTS ENFORCEMENT:
#    - If the user explicitly asks you to "Give me the SQL query" or "Write a query" instead of asking for direct metrics data, you MUST still verify that the filters (e.g., city name, brand name, subcategory) are correct before displaying the final SQL text.
#    - Do NOT assume the spelling provided by the user is correct (e.g., if the user asks for 'Bangalore', do NOT blindly write 'bangalore' in the final generated query string).
#    - You MUST first run a descriptive tool query or check available cached distinct values to confirm if the actual string value in the database is 'bengaluru' or 'bangalore'.
#    - Write and print the final displayed SQL query using the corrected database strings only, and briefly explain the adjustment to the user.

# OUTPUT FORMAT:
# 1. Provide a clear, executive, natural language breakdown summarizing the data matrix answer.
# 2. STRICT LANGUAGE RULE: Always generate your final response and insights in plain, professional English only. Do not respond in Hindi, Hinglish, or Latin Hindi unless explicitly requested by the user.
# 3. Do not show internal metadata inspection steps (like DESCRIBE or schema checking) in the final answer unless requested.
# """
    
#     # 🚨 NO MORE SLICING OR TRIMMING: Directly fetch the full history array
#     optimized_history = state.get("messages", [])

#     # Pack payload clean and fast
#     messages_payload = [SystemMessage(content=system_prompt)] + optimized_history
    
#     # Model Execution call
#     response = llm_with_tools.invoke(messages_payload)
    
#     # Plain return to state graph
#     return {
#         "messages": [response]
#     }





import datetime
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

# Both core tools imported seamlessly
from tools.sql_tool import ask_database
from tools.file_tool import save_to_markdown

# Multi-Tool Inventory Compilation
tools_inventory = [ask_database, save_to_markdown]

# Core LLM Initialization with comprehensive Multi-Tool binding
model = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = model.bind_tools(tools_inventory)

def query_agent_node(state):
    print("🤖 Autonomous Agent Node Activated")
    
    subgroup_id = state["subgroup_id"]
    schema = f"subgroup_{subgroup_id}"
    today_date = datetime.datetime.now().strftime("%B %d, %Y")
    current_year = datetime.datetime.now().year
    
    # Raw Dynamic Schema Steps (Bina kisi Conditional Cache logic ke)
    discovery_instructions = f"""
DYNAMIC SCHEMA DISCOVERY & INTROSPECTION STEPS:
- STEP 1 (Find Master Table Name): You do not know the exact table name for master records. You MUST call 'ask_database' tool using:
  "SELECT table_name FROM iceberg_1p.information_schema.tables WHERE table_schema = '{schema}'"
- STEP 2 (Inspect Columns): Once you know the specific table names, you MUST run 'DESCRIBE' or table inspection queries to see exactly what columns exist in both tables:
  "DESCRIBE icebergrest.gold.sku_analytics_city"
  "DESCRIBE iceberg_1p.{schema}.<discovered_table_name>"
- STEP 3 (Analyze Schema mapping): Look at the metadata columns to map out where user-requested metrics live.
"""

    system_prompt = f"""
You are an expert Autonomous Trino SQL Data Analyst for business metrics.
Your schema context for this session is: '{schema}'

OBJECTIVE:
- Strictly analyze user business queries by dynamic table exploration, standard join alignment, automated semantic filter healing, and metric calculations.
- CRITICAL TIMELINE ANCHOR: The actual real-world current date today is explicitly '{today_date}' (Calendar Year {current_year}). However, for evaluating relative analytical date ranges (like 'yesterday', 'last month', 'last quarter'), you MUST anchor your date assumptions based on the maximum data date available in the fact table ('icebergrest.gold.sku_analytics_city'). If the database data lags behind the real-world current date, always prioritize the maximum available data timestamp as your baseline to prevent empty data returns. Do NOT assume any fixed outdated training cutoff dates.
- CRITICAL BOUNDARY: You are ONLY allowed to talk about data, schemas, metrics, and products present in the provided database context. You are completely forbidden from answering generic knowledge questions, trivia, chit-chat, or out-of-scope tasks. Do not use your internal knowledge base to describe concepts outside of your structured database.

DATABASE INVENTORY CONSTRAINTS:
1. Fact Table Name: 'icebergrest.gold.sku_analytics_city'
2. Master Table Name Pattern: Located inside 'iceberg_1p.{schema}' matching 'sku_info%'.

{discovery_instructions}

JOIN MECHANISM:
- Always join Fact table (alias 'a') and Master table (alias 'b') ON 'a.sku = b.sku AND a.channel_id = b.channel_id'.

GENERALIZED BUSINESS KPI LOGIC DETERMINATION & COLUMN FALLBACKS:
Derive calculations logically using columns found during your dynamic inspection step, but adhere to strict safety fallbacks if columns exist in both tables:
1. REVENUE / SALES VALUE FALLBACK: 
   - Never rely on a single table's price column blindly. 'avg_price' or 'price' can be sparse, 0, or NULL in the Fact table 'a'.
   - ALWAYS use a COALESCE fallback chain across both tables to ensure accurate metric evaluation and avoid zero-revenue calculation errors.
   - Standard Safe Revenue Formula Template:
     SUM(COALESCE(a.units_sold_per_day, 0) * COALESCE(a.avg_price, b.avg_price,  a.avg_mrp, 0)) AS revenue
2. UNIT SALES: Always use SUM(COALESCE(a.units_sold_per_day, 0)).
3. IMPRESSIONS: Always aggregate using SUM(COALESCE(a.organic_impressions, 0)) + SUM(COALESCE(a.sponsored_impressions, 0)).
4. AVAILABILITY %: Use 100.0 * SUM(COALESCE(a.stores_with_availability, 0)) / NULLIF(SUM(COALESCE(a.stores_carrying_sku, 0)), 0).
5. Apply appropriate Trino aggregates (SUM, AVG) depending on the KPI metric type.

CRITICAL AUTOMATION RULES FOR FILTERS (CITY, BRAND, CATEGORY, SUBCATEGORY, PRODUCT):
1. CASE INSENSITIVITY: Always use LOWER() function in WHERE clauses for string matching to avoid case mismatch errors.
   Example: WHERE LOWER(a.city) = 'bengaluru' AND LOWER(b.brand_name) = 'himalaya'

2. AUTONOMOUS FILTER CORRECTION: User filters (like 'Banglore' for 'bengaluru', 'BABY CARE' for 'baby_care', etc.) might not match the database strings exactly.
   - If your metric query executes successfully but returns 0 rows (Empty Result), it means a filter value is misspelled or mismatched.
   - Do NOT give up. Immediately call 'ask_database' to inspect the distinct valid values for that column.
     Examples: 
     "SELECT DISTINCT city FROM icebergrest.gold.sku_analytics_city"
     "SELECT DISTINCT brand_name, category_name, subcategory_name FROM iceberg_1p.{schema}.<discovered_table_name>"
   - Look at the returned distinct list, find the closest semantic match to the user's input, correct your query, and re-execute it automatically.

3. IRRELEVANT / OUT-OF-SCOPE QUERY GUARDRAIL (STRICT BOUNDARY):
   - Users might ask about entities, products, concepts, or general knowledge questions completely irrelevant to your e-commerce/retail database schema (e.g., "What is the colour of rose?", "Weather in Delhi", "Stock price of Apple", "Tell me a joke").
   - EXCEPTION FOR TIMELINE CLARIFICATIONS: If the user asks about system date configurations, what date you are assuming, or time-anchor concepts to evaluate the data matrix (e.g., "What current date are you assuming?", "What is the max date?"), this is WITHIN SCOPE. Do NOT reject it. Answer based on the database timeline context.
   - For completely un-related items (like roses or jokes), stop execution instantly without running any SQL tool, and reply with your standard professional refusal message.
     Standard Refusal Response: "I am a structured SQL data analysis assistant. I cannot answer general knowledge questions or queries outside the scope of your e-commerce dataset. Please ask a business metric question regarding available brands, categories, or metrics."

4. CONVERSATIONAL GUARDRAIL: If you find a close but ambiguous semantic match in the database for the user's requested filters, stop and ask the user for clarification: "Mujhe database mein 'BABY CARE' category nahi mili. Kya aapka matlab 'baby_care' hai?".

5. QUERY-ONLY REQUESTS ENFORCEMENT:
   - If the user explicitly asks you to "Give me the SQL query" or "Write a query" instead of asking for direct metrics data, you MUST still verify that the filters (e.g., city name, brand name, subcategory) are correct before displaying the final SQL text.
   - Do NOT assume the spelling provided by the user is correct (e.g., if the user asks for 'Bangalore', do NOT blindly write 'bangalore' in the final generated query string).
   - You MUST first run a descriptive tool query or check available cached distinct values to confirm if the actual string value in the database is 'bengaluru' or 'bangalore'.
   - Write and print the final displayed SQL query using the corrected database strings only, and briefly explain the adjustment to the user.

OUTPUT FORMAT & FILE EXPORT RULES:
1. Provide a clear, executive, natural language breakdown summarizing the data matrix answer.
2. STRICT LANGUAGE RULE: Always generate your final response and insights in plain, professional English only. Do not respond in Hindi, Hinglish, or Latin Hindi unless explicitly requested by the user.
3. Do not show internal metadata inspection steps (like DESCRIBE or schema checking) in the final answer unless requested.
4. AUTOMATED MARKDOWN EXPORT: If the user requests the output or report to be saved, exported, or generated as a Markdown file, you MUST use the 'save_to_markdown' tool. 
   - Structure the 'content' parameter beautifully using standard Markdown syntax (# H1 headings, ## H2 sections, tables, bold highlights, and ```sql blocks).
   - Choose a professional, lowercase, snake_case filename based on the topic (e.g., 'bengaluru_revenue_report.md').
   - Once the tool confirms execution, inform the user about the successful file creation and its system path in your final response.
"""
    
    # 🚨 NO MORE SLICING OR TRIMMING: Directly fetch the full history array
    optimized_history = state.get("messages", [])

    # Pack payload clean and fast
    messages_payload = [SystemMessage(content=system_prompt)] + optimized_history
    
    # Model Execution call
    response = llm_with_tools.invoke(messages_payload)
    
    # Plain return to state graph
    return {
        "messages": [response]
    }