import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

OLLAMA_URL = "https://ollama.com/api/chat"


SCHEMA = """
Table: retail_sales

Columns:
Invoice VARCHAR(20)
StockCode VARCHAR(20)
Description VARCHAR(255)
Quantity INT
InvoiceDate DATETIME
Price DECIMAL(10,3)
Customer_ID VARCHAR(20)
Country VARCHAR(100)
Revenue DECIMAL(12,3)
Sales_Year INT
Sales_Month INT
Month_Name VARCHAR(20)
Day_Name VARCHAR(20)
Hour INT
Sales_period VARCHAR(7)
"""


def generate_sql(question):

    prompt = f"""
You are a SQL analyst for a retail business.

You have access to this MySQL table:

{SCHEMA}

Your job is to convert the user's business question into
ONE safe, read-only MySQL SELECT query.

Rules:
1. Only generate SELECT queries.
2. Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or TRUNCATE.
3. Use only the retail_sales table.
4. Use only columns that exist in the schema.
5. Return ONLY the SQL query.
6. Do not use markdown code fences.
7. Use MySQL syntax.

User question:
{question}
"""

    headers = {
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-oss:20b",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        headers=headers,
        json=data
    )

    response.raise_for_status()

    result = response.json()

    sql = result["message"]["content"].strip()

    # Remove markdown fences if the model accidentally adds them
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql


if __name__ == "__main__":

    question = "Which country generated the highest revenue?"

    print("\n========== USER QUESTION ==========")
    print(question)

    sql = generate_sql(question)

    print("\n========== GENERATED SQL ==========")
    print(sql)