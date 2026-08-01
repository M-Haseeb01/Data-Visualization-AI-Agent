"""
Data Visualization Agent
------------------------

Uses Groq + LangChain + pandas to analyze uploaded datasets
and generate visualizations.
"""

import os
import pandas as pd

from langchain_experimental.agents.agent_toolkits import (
    create_pandas_dataframe_agent,
)

from langchain_groq import ChatGroq

from core import (
    GROQ_MODEL,
    new_chart_path,
    build_prompt,
)


# ============================================================
# Build Agent
# ============================================================

def build_agent(
    df: pd.DataFrame,
    api_key: str,
):

    print("Creating Groq model...")

    llm = ChatGroq(
        model=GROQ_MODEL,
        api_key=api_key,
        temperature=0,
    )

    print("Creating Data Visualization Agent...")

    agent = create_pandas_dataframe_agent(
        llm,
        df,
        agent_type="tool-calling",
        verbose=True,
        allow_dangerous_code=True,
        max_iterations=3,
    )

    print("Agent ready.")

    return agent


# ============================================================
# Ask Agent
# ============================================================

def ask_agent(
    df: pd.DataFrame,
    question: str,
    api_key: str,
):

    print("\n==========================================")
    print("DATA VISUALIZATION AGENT")
    print("==========================================")
    print("Question:", question)
    print("Rows:", len(df))
    print("Columns:", list(df.columns))

    agent = build_agent(
        df=df,
        api_key=api_key,
    )

    chart_path = new_chart_path()

    prompt = build_prompt(
        question=question,
        chart_path=chart_path,
    )

    print("Calling Groq...")

    try:

        result = agent.invoke(
            {
                "input": prompt
            }
        )

        answer = result.get(
            "output",
            "I couldn't generate an answer.",
        )

    except Exception as e:

        print("Agent error:", repr(e))

        answer = f"⚠️ Agent error: {e}"

    # Check chart
    if os.path.exists(chart_path):
        final_chart = chart_path
    else:
        final_chart = None

    print("Chart:", final_chart)
    print("==========================================")

    return answer, final_chart
