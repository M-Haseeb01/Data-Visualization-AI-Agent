
"""
SQL Data Analysis Agent
-----------------------

Professional Gradio interface for querying SQLite databases.
"""

import gradio as gr

from core import GROQ_API_KEY, save_database
from agent import ask_agent


# ============================================================
# Main Function
# ============================================================

def analyze_database(
    database_file,
    question,
    history,
):

    history = history or []

    # --------------------------------------------------------
    # API Key
    # --------------------------------------------------------

    if not GROQ_API_KEY:

        history.append({
            "role": "user",
            "content": question,
        })

        history.append({
            "role": "assistant",
            "content": (
                "GROQ_API_KEY was not found. "
                "Please add it to your environment variables."
            ),
        })

        return history, ""

    # --------------------------------------------------------
    # Question
    # --------------------------------------------------------

    if not question or not question.strip():

        return history, ""

    # --------------------------------------------------------
    # Database
    # --------------------------------------------------------

    try:

        database_path = save_database(database_file)

        print("Database loaded:")
        print(database_path)

    except Exception as e:

        history.append({
            "role": "user",
            "content": question,
        })

        history.append({
            "role": "assistant",
            "content": f"Database error: {e}",
        })

        return history, ""

    # --------------------------------------------------------
    # Agent
    # --------------------------------------------------------

    try:

        answer = ask_agent(
            database_path=database_path,
            question=question,
            api_key=GROQ_API_KEY,
        )

    except Exception as e:

        answer = f"Agent error: {e}"

    # --------------------------------------------------------
    # Chat
    # --------------------------------------------------------

    history.append({
        "role": "user",
        "content": question,
    })

    history.append({
        "role": "assistant",
        "content": answer,
    })

    return history, ""


# ============================================================
# Clear
# ============================================================

def clear_all():

    return [], ""


# ============================================================
# CSS
# ============================================================

CUSTOM_CSS = """

.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
}

.app-header {
    text-align: center;
    padding: 28px 0 4px 0;
}

.app-subtitle {
    text-align: center;
    color: #6b7280;
    margin-bottom: 28px;
    font-size: 15px;
}

.panel {
    border-radius: 10px;
    border: 1px solid #e5e7eb !important;
    padding: 4px;
}

.section-label {
    font-weight: 600;
    font-size: 13px;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 4px;
}

.example-list {
    color: #4b5563;
    font-size: 14px;
    line-height: 1.8;
}

.footer-note {
    color: #9ca3af;
    font-size: 12px;
}

"""


# ============================================================
# UI
# ============================================================

def build_ui():

    with gr.Blocks(
        title="SQL Data Analysis Agent",
    ) as demo:

        # ====================================================
        # Header
        # ====================================================

        gr.Markdown(
            """
            <div class="app-header">

            # SQL Data Analysis Agent

            </div>

            <div class="app-subtitle">

            Upload a SQLite database and ask questions
            using natural language.

            </div>
            """
        )

        # ====================================================
        # Main
        # ====================================================

        with gr.Row(equal_height=False):

            # ------------------------------------------------
            # Left
            # ------------------------------------------------

            with gr.Column(
                scale=1,
                min_width=280,
                elem_classes="panel",
            ):

                gr.Markdown(
                    "<div class='section-label'>Database</div>"
                )

                database_file = gr.File(
                    label="Upload SQLite Database",
                    file_types=[
                        ".db",
                        ".sqlite",
                        ".sqlite3",
                    ],
                    type="filepath",
                )

                gr.Markdown(
                    """
                    <span class="footer-note">

                    Supported formats:<br>
                    `.db` · `.sqlite` · `.sqlite3`

                    </span>
                    """
                )

                gr.Markdown(
                    """
                    <div class='section-label'
                    style='margin-top:20px;'>
                    Example questions
                    </div>
                    """
                )

                gr.Markdown(
                    """
                    <div class="example-list">

                    - How many customers are there?
                    - Show the top 10 products by sales.
                    - What is the total revenue?
                    - Which customer spent the most?
                    - Show sales by month.
                    - What are the available tables?

                    </div>
                    """
                )

            # ------------------------------------------------
            # Right
            # ------------------------------------------------

            with gr.Column(
                scale=2,
                elem_classes="panel",
            ):

                gr.Markdown(
                    "<div class='section-label'>Conversation</div>"
                )

                chatbot = gr.Chatbot(
                    label=None,
                    show_label=False,
                    height=460,
                )

                with gr.Row():

                    question_box = gr.Textbox(
                        placeholder=(
                            "Ask a question about your database..."
                        ),
                        show_label=False,
                        scale=5,
                        container=False,
                    )

                    ask_button = gr.Button(
                        "Run Query",
                        variant="primary",
                        scale=1,
                    )

                clear_button = gr.Button(
                    "Clear conversation",
                    size="sm",
                    variant="secondary",
                )

        # ====================================================
        # Events
        # ====================================================

        ask_button.click(
            fn=analyze_database,
            inputs=[
                database_file,
                question_box,
                chatbot,
            ],
            outputs=[
                chatbot,
                question_box,
            ],
        )

        question_box.submit(
            fn=analyze_database,
            inputs=[
                database_file,
                question_box,
                chatbot,
            ],
            outputs=[
                chatbot,
                question_box,
            ],
        )

        clear_button.click(
            fn=clear_all,
            inputs=[],
            outputs=[
                chatbot,
                question_box,
            ],
        )

    return demo


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("       SQL DATA ANALYSIS AGENT")
    print("==========================================")
    print("Starting application...")
    print()

    if not GROQ_API_KEY:

        print("WARNING: GROQ_API_KEY not found.")

    else:

        print("Groq API key loaded from environment.")

    demo = build_ui()

    demo.launch(
        theme=gr.themes.Soft(
            primary_hue="slate",
            neutral_hue="slate",
        ),
        css=CUSTOM_CSS,
    )
