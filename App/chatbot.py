import os
import re
import requests
from dotenv import load_dotenv

from sql_generator import generate_sql
from query_database import execute_query

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_URL = "https://ollama.com/api/chat"


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


def generate_final_answer(question, sql, results):

    prompt = f"""
You are an AI Business Decision Assistant.

Answer the user's business question using ONLY the MySQL result provided below.

USER QUESTION:
{question}

SQL QUERY:
{sql}

DATABASE RESULT:
{results}

Rules:
1. Give a clear and concise business answer.
2. Do not invent information.
3. Do not mention that you are an AI unless necessary.
4. Do not mention Python, Ollama, or the database unless necessary.
5. If the result contains a monetary revenue value, format it clearly.
6. Use £ because this retail dataset uses British pounds.
7. For large revenue values, use millions when appropriate.
8. Briefly explain the result.
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

    return result["message"]["content"].strip()


def ask_chatbot(question):

    print("\n========== USER QUESTION ==========")
    print(question)

    # 1. Generate SQL
    sql = generate_sql(question)

    print("\n========== GENERATED SQL ==========")
    print(sql)

    # 2. Safety check
    if not is_safe_sql(sql):
        return {
            "success": False,
            "error": "The generated SQL was blocked because it is not a safe read-only query."
        }

    print("\n========== SQL SAFETY ==========")
    print("Safe SELECT query ✅")

    # 3. Execute SQL
    try:
        results = execute_query(sql)

    except Exception as error:
        return {
            "success": False,
            "error": f"Database error: {error}"
        }

    print("\n========== MYSQL RESULT ==========")
    print(results)

    # 4. Generate natural-language answer
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


if __name__ == "__main__":

    question = "Which country generated the highest revenue?"

    result = ask_chatbot(question)

    print("\n========== FINAL RESULT ==========")
    print(result)