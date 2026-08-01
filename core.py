"""
Core utilities for Data Visualization Agent.
"""

import os
import uuid

import pandas as pd
import matplotlib

from dotenv import load_dotenv


# ============================================================
# Environment
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

GROQ_MODEL = "llama-3.3-70b-versatile"

CHART_DIR = "charts"
os.makedirs(CHART_DIR, exist_ok=True)


# ============================================================
# Load CSV / Excel
# ============================================================

def load_data(file_obj) -> pd.DataFrame:
    """
    Load CSV or Excel file into a pandas DataFrame.
    """

    if file_obj is None:
        raise ValueError("Please upload a CSV or Excel file.")

    if isinstance(file_obj, str):
        path = file_obj
    else:
        path = file_obj.name

    extension = os.path.splitext(path)[1].lower()

    if extension == ".csv":
        df = pd.read_csv(path)

    elif extension in [".xlsx", ".xls"]:
        df = pd.read_excel(path)

    else:
        raise ValueError(
            "Unsupported file type. Please upload CSV or Excel."
        )

    if df.empty:
        raise ValueError("The uploaded file contains no data.")

    return df


# ============================================================
# Chart Path
# ============================================================

def new_chart_path() -> str:

    filename = f"chart_{uuid.uuid4().hex}.png"

    return os.path.join(
        CHART_DIR,
        filename,
    )


# ============================================================
# Agent Prompt
# ============================================================

def build_prompt(question: str, chart_path: str) -> str:

    return f"""
You are a professional data analysis and visualization assistant.

You have access to a pandas DataFrame called `df`.

USER REQUEST:
{question}

INSTRUCTIONS:

1. Analyze the data using pandas and Python.

2. If the user asks for a chart, graph, plot, or visualization:
   - Use matplotlib.
   - Do not use plt.show().
   - Save the chart to:

{chart_path}

   Use:

plt.tight_layout()
plt.savefig(r"{chart_path}")
plt.close()

3. Choose an appropriate chart type based on the user's request.

4. Add meaningful titles and axis labels to charts.

5. If the user asks a normal data question, provide the answer
   directly without creating a chart.

6. Keep the final response concise and understandable.

7. Never expose internal reasoning or unnecessary Python code.
"""
