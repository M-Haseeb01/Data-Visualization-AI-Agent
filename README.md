# Data-Visualization-Agent

An AI-powered Data Visualization and Analysis Agent that allows users to upload CSV or Excel datasets and interact with their data using natural language. The application uses an LLM-powered LangChain agent to analyze datasets, perform calculations, and automatically generate visualizations using Python and Matplotlib.

---

## Features

- Upload CSV and Excel files (`.csv`, `.xlsx`, `.xls`)
- Ask natural-language questions about datasets
- AI-powered data analysis using Groq-hosted LLMs
- Automatic pandas-based data processing
- Generate charts and visualizations from natural-language requests
- Create bar charts, line charts, and other visualizations
- Display generated charts directly in the interface
- Professional Gradio web interface
- Deployable on Hugging Face Spaces

---

## Working Flow

```text
CSV / Excel File
       │
       ▼
Dataset Loading (Pandas)
       │
       ▼
Pandas DataFrame
       │
       ▼
LangChain DataFrame Agent
       │
       ▼
Groq LLM (Llama)
       │
       ▼
Understand User Request
       │
       ▼
Generate & Execute Python
       │
       ├──────────────► Pandas Data Analysis
       │
       └──────────────► Matplotlib Visualization
                              │
                              ▼
                       Generated Chart
                              │
                              ▼
                    Final Answer + Chart
```

---

## Technology Stack

- Python
- Gradio
- LangChain
- Pandas
- Matplotlib
- Groq
- Llama
- OpenPyXL
- Hugging Face Spaces

---

## Installation

```bash
git clone https://github.com/your-username/Data-Visualization-Agent.git
cd Data-Visualization-Agent
pip install -r requirements.txt
```

---

## Usage

```bash
python app.py
```

Then open the local Gradio URL in your browser, upload a dataset, and start asking questions.

---

## Example Queries

```
What is the average revenue?

Which category has the highest sales?

Show monthly revenue as a line chart.

Create a bar chart of sales by region.

What are the main trends in this dataset?
```
---

## Demo

