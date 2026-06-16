# LangGraph Analytics Copilot 🤖📊

An expert Autonomous Trino SQL Data Analyst built with LangGraph to inspect, query, and analyze complex retail and e-commerce business metrics dynamically.

## 🚀 Overview

The **LangGraph Analytics Copilot** is an intelligent data agent designed to bridge the gap between natural language business queries and Trino SQL databases. Built on top of LangGraph, it leverages stateful, multi-turn agent workflows to explore database schemas dynamically, apply automated semantic filters, calculate key business KPIs, and safeguard against out-of-scope requests.

---

## ✨ Key Features

### 1. Dynamic Schema Discovery & Metadata Caching
- **Live Inspection:** Automatically runs schema discovery using Trino `DESCRIBE` and catalog inspection if a metadata cache miss occurs.
- **Smart Mapping:** Dynamically identifies Fact tables (`icebergrest.gold.sku_analytics_city`) and Master tables (`iceberg_1p.{schema}.sku_info%`) to establish accurate relationships.

### 2. Robust KPI Formulation & Fallback Chains
Ensures accurate metric evaluation even with sparse or missing data using strict `COALESCE` fallback chains:
- **Revenue / Sales Value:** `SUM(COALESCE(a.units_sold_per_day, 0) * COALESCE(a.avg_price, b.avg_price, a.avg_mrp, 0))`
- **Unit Sales:** `SUM(COALESCE(a.units_sold_per_day, 0))`
- **Impressions:** `SUM(COALESCE(a.organic_impressions, 0)) + SUM(COALESCE(a.sponsored_impressions, 0))`
- **Availability %:** `100.0 * SUM(COALESCE(a.stores_with_availability, 0)) / NULLIF(SUM(COALESCE(a.stores_carrying_sku, 0)), 0)`

### 3. Autonomous Filter Healing & Correction
- **Case Insensitivity:** Automatically wraps filters in `LOWER()` to prevent case mismatch errors.
- **Empty Result Recovery:** If a query executes successfully but returns 0 rows, the agent autonomously queries `DISTINCT` values (e.g., checking available cities or brands) to find the closest semantic match and self-heals the query.

### 4. Enterprise Guardrails & Context Anchors
- **Out-of-Scope Guardrail:** Rejects completely irrelevant queries (e.g., *"What is the color of a rose?"* or *"Apple stock price"*) politely if no semantic match exists in the database.
- **Conversational Clarification:** Halts and asks for user confirmation if a filter match is ambiguous (e.g., *"Mujhe 'BABY CARE' category nahi mili. Kya aapka matlab 'baby_care' hai?"*).
- **Timeframe Anchor:** Anchored to look at the maximum date present in the database fact table for relative calculations (*yesterday, last month, current quarter*).

---

## 🏗️ Architecture Workflow

```text
[ User Query ] ──> [ Out-of-Scope Guardrail ] ──> [ Dynamic Schema Discovery ]
                                                            │
  ┌─────────────────────────────────────────────────────────┘
  ▼
[ SQL Generation & KPI Joins ] ──> [ Execution ] ──> [ Empty Rows? ] ──► (Yes) ──► [ Autonomous Filter Healing ]
                                           │                                                 │
                                         (No)                                                ▼
                                           │                                       [ Recalibrate & Re-execute ]
                                           ▼
                                [ Professional English Insights ]


**## 🛠️ Installation & Setup
**
1. **Clone the Repository:**
```bash
   git clone [https://github.com/pallavibhan/langgraph-analytics-copilot.git](https://github.com/pallavibhan/langgraph-analytics-copilot.git)
   cd langgraph-analytics-copilot


   Environment Setup:
Create a .env file in the root directory and configure your Trino connection details and LLM API keys:

Code snippet
   TRINO_HOST=your-trino-host
   TRINO_PORT=8080
   TRINO_USER=admin name
   TRINO_CATALOG=icebergrest
   OPENAI_API_KEY=your-openai-key
   
1. Install Dependencies:
Bash
   pip install -r requirements.txt

   Run the Copilot:

2. Bash
   python main.py


📝 Usage Examples
Standard Business Query
User: "What was the total revenue and availability % for Himalaya brand in Bengaluru last week?"

Copilot Action: Joins the fact table with the discovered master table on sku and channel_id, applies LOWER(city) = 'bengaluru', calculates metrics via fallback chains, and outputs a clean executive breakdown.

Out-of-Scope Protection Example
User: "What is the colour of rose?"

Copilot Response: "Mujhe database mein 'rose' se related koi brand, category, ya product nahi mila. Main aapko is subgroup mein available data aur metrics hi provide kar sakta hoon. Kya aap inme se kuch poochna chahte hain?"

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an issue for bugs and feature requests.   
