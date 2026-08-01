"""
SQL Agent
---------

LangChain SQL agent powered by Groq.
"""

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

from core import GROQ_MODEL


def build_agent(database_path, api_key):

    print("Connecting to database...")

    db = SQLDatabase.from_uri(
        f"sqlite:///{database_path}"
    )

    print("Creating Groq model...")

    llm = ChatGroq(
        model=GROQ_MODEL,
        api_key=api_key,
        temperature=0,
    )

    print("Creating SQL agent...")

    agent = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="tool-calling",
        verbose=True,
        max_iterations=5,
    )

    return agent


def ask_agent(database_path, question, api_key):

    agent = build_agent(
        database_path=database_path,
        api_key=api_key,
    )

    prompt = f"""
You are a professional SQL data analyst.

Answer the user's question using the connected SQL database.

User question:
{question}

Instructions:

- Inspect the database schema when necessary.
- Write correct SQL queries.
- Execute the SQL query using the available tools.
- Do not invent table names or columns.
- Base your answer only on the database results.
- Keep the final answer concise and easy to understand.
- If the question cannot be answered from the database,
  clearly explain why.
"""

    try:

        result = agent.invoke(
            {
                "input": prompt
            }
        )

        return result.get(
            "output",
            "I couldn't generate an answer."
        )

    except Exception as e:

        print("SQL Agent error:", repr(e))

        return f"Agent error: {e}"
