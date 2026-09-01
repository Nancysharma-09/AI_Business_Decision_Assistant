import os
import re
import requests
from dotenv import load_dotenv

from sql_generator import generate_sql
from query_database import execute_query

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_URL = "https://ollama.com/api/chat"


# =========================================================
# SQL SAFETY
# =========================================================

def is_safe_sql(sql):
    """Allow only read-only SELECT queries."""

    sql_clean = sql.strip().lower()

    if not sql_clean.startswith("select"):
        return False

    blocked_commands = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "replace",
        "grant",
        "revoke"
    ]

    for command in blocked_commands:
        if re.search(rf"\b{command}\b", sql_clean):
            return False

    return True


# =========================================================
# COUNTRY DETECTION
# =========================================================

COUNTRY_NAMES = [
    "USA",
    "United States",
    "UK",
    "United Kingdom",
    "Germany",
    "France",
    "Netherlands",
    "EIRE",
    "Ireland",
    "Spain",
    "Belgium",
    "Switzerland",
    "Portugal",
    "Australia",
    "Japan",
    "Canada",
    "Italy",
    "Norway",
    "Sweden",
    "Denmark",
    "Finland",
    "Austria",
    "Poland",
    "Brazil",
    "Singapore",
]


def detect_country_question(question):
    """
    Detect whether the user entered a short country-only
    question such as:
        USA
        UK
        Germany
        What about USA
    """

    cleaned = question.strip().lower()

    # Remove common conversational phrases
    cleaned = re.sub(
        r"^(what about|how about|tell me about|show me|"
        r"give me|what is|what's)\s+",
        "",
        cleaned
    )

    for country in COUNTRY_NAMES:

        country_lower = country.lower()

        if cleaned == country_lower:
            return country

    return None


# =========================================================
# COUNTRY SUMMARY QUERY
# =========================================================

def generate_country_summary_sql(country):

    # Convert common names to the exact dataset values

    country_mapping = {
        "USA": "USA",
        "United States": "USA",
        "UK": "United Kingdom",
        "United Kingdom": "United Kingdom",
        "Germany": "Germany",
        "France": "France",
        "Netherlands": "Netherlands",
        "EIRE": "EIRE",
        "Ireland": "EIRE",
        "Spain": "Spain",
        "Belgium": "Belgium",
        "Switzerland": "Switzerland",
        "Portugal": "Portugal",
        "Australia": "Australia",
        "Japan": "Japan",
        "Canada": "Canada",
        "Italy": "Italy",
        "Norway": "Norway",
        "Sweden": "Sweden",
        "Denmark": "Denmark",
        "Finland": "Finland",
        "Austria": "Austria",
        "Poland": "Poland",
        "Brazil": "Brazil",
        "Singapore": "Singapore",
    }

    dataset_country = country_mapping.get(country, country)

    # Escape single quotes safely
    dataset_country = dataset_country.replace("'", "''")

    sql = f"""
SELECT
    COUNT(DISTINCT Invoice) AS total_invoices,
    ROUND(SUM(Revenue), 2) AS total_revenue
FROM retail_sales
WHERE Country = '{dataset_country}';
"""

    return sql.strip()


# =========================================================
# FINAL AI ANSWER
# =========================================================

def generate_final_answer(question, sql, results):

    prompt = f"""
You are an AI Business Decision Assistant for a retail analytics dashboard.

Answer the user's business question using ONLY the MySQL result provided below.

USER QUESTION:
{question}

SQL QUERY:
{sql}

DATABASE RESULT:
{results}

IMPORTANT RULES:

1. Give a direct business answer first.
2. Never ask the user to manually calculate anything.
3. Never tell the user to add numbers from raw database rows.
4. If the result contains an aggregate such as SUM, COUNT, or AVG, use that aggregate directly.
5. Do not invent information.
6. Do not mention Python, Ollama, SQL, MySQL, or database implementation details unless absolutely necessary.
7. Use British pounds (£) for revenue.
8. Format large revenue values clearly:
   - £8,366.86
   - £17.87 million
9. For country questions, present the result as a short sales snapshot.
10. Mention the most important metric first.
11. Keep the answer concise but useful.
12. Do not repeat the user's question.

If the result contains:
- total_revenue → report it as revenue
- total_invoices → report it as invoices

For a country summary, use this style:

◈ AI Insight

[Country] — Sales Snapshot

The country generated **£X** in revenue across **Y invoices**.

Then add one short business interpretation if the data supports it.
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
        json=data,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["message"]["content"].strip()


# =========================================================
# MAIN CHATBOT
# =========================================================

def ask_chatbot(question):

    print("\n========== USER QUESTION ==========")
    print(question)

    # -----------------------------------------------------
    # 1. Detect simple country questions
    # -----------------------------------------------------

    country = detect_country_question(question)

    if country:

        print("\n========== COUNTRY DETECTED ==========")
        print(country)

        sql = generate_country_summary_sql(country)

        print("\n========== GENERATED SQL ==========")
        print(sql)

    else:

        # -------------------------------------------------
        # 2. Generate normal SQL using the AI SQL generator
        # -------------------------------------------------

        sql = generate_sql(question)

        print("\n========== GENERATED SQL ==========")
        print(sql)

    # -----------------------------------------------------
    # 3. SQL SAFETY CHECK
    # -----------------------------------------------------

    if not is_safe_sql(sql):

        return {
            "success": False,
            "error": (
                "The generated SQL was blocked because "
                "it is not a safe read-only query."
            )
        }

    print("\n========== SQL SAFETY ==========")
    print("Safe SELECT query ✅")

    # -----------------------------------------------------
    # 4. Execute SQL
    # -----------------------------------------------------

    try:

        results = execute_query(sql)

    except Exception as error:

        return {
            "success": False,
            "error": f"Database error: {error}"
        }

    print("\n========== MYSQL RESULT ==========")
    print(results)

    # -----------------------------------------------------
    # 5. Generate natural-language answer
    # -----------------------------------------------------

    try:

        final_answer = generate_final_answer(
            question,
            sql,
            results
        )

    except Exception as error:

        return {
            "success": False,
            "error": f"AI response error: {error}"
        }

    print("\n========== AI ANSWER ==========")
    print(final_answer)

    return {
        "success": True,
        "question": question,
        "sql": sql,
        "results": results,
        "answer": final_answer
    }


# =========================================================
# DIRECT TEST
# =========================================================

if __name__ == "__main__":

    question = "USA"

    result = ask_chatbot(question)

    print("\n========== FINAL RESULT ==========")
    print(result)