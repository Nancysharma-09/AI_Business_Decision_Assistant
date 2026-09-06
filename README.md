# 🤖 AI Business Decision Assistant

### Turn business questions into data-driven answers.

<p align="center">
  <img src="C:\Users\DELL\Downloads\Logo.png" alt="AI Business Decision Assistant" width="450">
</p>

> A GenAI-powered retail analytics assistant that lets users ask business questions in natural language and receive data-backed insights.

---

## 🚀 What It Does

The assistant takes a question like:

**"Which country generates the most revenue?"**

and automatically:

**Question → SQL → Database → Result → AI Insight**

It uses a cloud-hosted **TiDB** database containing over 1 million retail transactions and generates safe, read-only SQL queries using **Ollama LLM**.

---

## 🧠 Built With

**Python** · **SQL** · **Power BI** · **Ollama** · **Streamlit** · **TiDB Cloud** · **Pandas**

---

## 🔐 Safe SQL Execution

The assistant validates generated queries before execution and allows only **read-only SELECT statements**.

Operations such as `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, and `TRUNCATE` are blocked.

---

## 📊 Business Analytics

The underlying retail data contains:

- **1,041,671** cleaned transactions
- **5,879** customers
- **£20.97M** total revenue

The project analyzes revenue, customers, products, countries, orders, and sales trends.

---

## 💬 Try It

Ask questions such as:

```text
What is the total revenue?
Which country generates the most revenue?
What are the top-selling products?
How has revenue changed over time?
🌐 Live AI Assistant

https://aibusinessdecisionassistant-pnji93sbm2bmf3trjfacgm.streamlit.app/

📈 Power BI Dashboard

Power BI provides the executive view of the retail business, while the AI assistant provides an interactive way to explore the data through natural-language questions.

🏗️ Architecture
Power BI
   ↓
Streamlit AI Assistant
   ↓
Ollama LLM
   ↓
SQL Generation
   ↓
SQL Safety Validation
   ↓
TiDB Cloud
   ↓
Business Data
   ↓
AI-Generated Insight
👩‍💻 Author
Nancy Sharma

Data Analyst | SQL | Power BI | Python | GenAI
