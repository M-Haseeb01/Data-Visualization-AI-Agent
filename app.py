"""
Data Visualization Agent
------------------------

Professional Gradio interface for analyzing CSV and Excel files.

Run:

    python3 app.py
"""

import gradio as gr

from core import GROQ_API_KEY, load_data
from agent import ask_agent


# ============================================================
# Main Chat Function
# ============================================================

def analyze_data(
    data_file,
    question,
    history,
):

    history = history or []

    # --------------------------------------------------------
    # Validate API key
    # --------------------------------------------------------

    if not GROQ_API_KEY:

        history.append(
            {
                "role": "user",
                "content": question,
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": (
                    "GROQ_API_KEY was not found. "
                    "Please add it to your .env file."
                ),
            }
        )

        return history, None, ""

    # --------------------------------------------------------
    # Validate question
    # --------------------------------------------------------

    if not question or not question.strip():

        return history, None, ""

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    try:

        df = load_data(data_file)

        print("\nDataset loaded successfully.")
        print("Shape:", df.shape)

    except Exception as e:

        history.append(
            {
                "role": "user",
                "content": question,
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": f"Error: {e}",
            }
        )

        return history, None, ""

    # --------------------------------------------------------
    # Run agent
    # --------------------------------------------------------

    try:

        answer, chart_path = ask_agent(
            df=df,
            question=question,
            api_key=GROQ_API_KEY,
        )

    except Exception as e:

        answer = f"Agent error: {e}"
        chart_path = None

    # --------------------------------------------------------
    # Update chat
    # --------------------------------------------------------

    history.append(
        {
            "role": "user",
            "content": question,
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    return history, chart_path, ""


# ============================================================
# Clear Function
# ============================================================

def clear_all():

    return [], None, ""


# ============================================================
# UI
# ============================================================

def build_ui():

    with gr.Blocks(
        title="Data Visualization Agent",
        theme=gr.themes.Soft(
            primary_hue="slate",
            neutral_hue="slate",
        ),
        css="""
        .gradio-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
        }

        .app-header {
            text-align: center;
            padding: 28px 0 4px 0;
            font-weight: 600;
            letter-spacing: -0.01em;
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
            line-height: 1.7;
        }

        .footer-note {
            color: #9ca3af;
            font-size: 12px;
        }
        """,
    ) as demo:

        # ====================================================
        # Header
        # ====================================================

        gr.Markdown(
            """
            <div class="app-header">

            # Data Visualization Agent

            </div>

            <div class="app-subtitle">

            Upload a dataset and explore it using natural language —
            summaries, calculations, and charts on demand.

            </div>
            """
        )

        # ====================================================
        # Main Layout
        # ====================================================

        with gr.Row(equal_height=False):

            # ------------------------------------------------
            # LEFT PANEL
            # ------------------------------------------------

            with gr.Column(
                scale=1,
                min_width=280,
                elem_classes="panel",
            ):

                gr.Markdown(
                    "<div class='section-label'>Dataset</div>"
                )

                data_file = gr.File(
                    label="Upload CSV or Excel",
                    file_types=[
                        ".csv",
                        ".xlsx",
                        ".xls",
                    ],
                    type="filepath",
                )

                gr.Markdown(
                    """
                    <span class="footer-note">
                    Supported formats: CSV, XLSX, XLS.<br>
                    Your API key is loaded from the local .env file.
                    </span>
                    """
                )

                gr.Markdown(
                    "<div class='section-label' style='margin-top:20px;'>Example questions</div>"
                )

                gr.Markdown(
                    """
                    <div class="example-list">

                    - What are the main trends in this data?
                    - What is the average revenue?
                    - Which category performs best?
                    - Create a bar chart of sales by category.
                    - Show monthly revenue as a line chart.

                    </div>
                    """
                )

            # ------------------------------------------------
            # RIGHT PANEL
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
                    height=420,
                )

                with gr.Row():

                    question_box = gr.Textbox(
                        placeholder="Ask a question about your dataset...",
                        show_label=False,
                        scale=5,
                        container=False,
                    )

                    ask_button = gr.Button(
                        "Analyze",
                        variant="primary",
                        scale=1,
                    )

                clear_button = gr.Button(
                    "Clear conversation",
                    size="sm",
                    variant="secondary",
                )

        # ====================================================
        # Chart Output
        # ====================================================

        with gr.Column(elem_classes="panel"):

            gr.Markdown(
                "<div class='section-label'>Visualization</div>"
            )

            chart_image = gr.Image(
                label=None,
                show_label=False,
                type="filepath",
                height=460,
            )

        # ====================================================
        # Events
        # ====================================================

        ask_button.click(
            fn=analyze_data,
            inputs=[
                data_file,
                question_box,
                chatbot,
            ],
            outputs=[
                chatbot,
                chart_image,
                question_box,
            ],
        )

        question_box.submit(
            fn=analyze_data,
            inputs=[
                data_file,
                question_box,
                chatbot,
            ],
            outputs=[
                chatbot,
                chart_image,
                question_box,
            ],
        )

        clear_button.click(
            fn=clear_all,
            inputs=[],
            outputs=[
                chatbot,
                chart_image,
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
    print("      DATA VISUALIZATION AGENT")
    print("==========================================")
    print("Starting application...")
    print()

    if not GROQ_API_KEY:
        print("WARNING: GROQ_API_KEY not found.")
        print("Add GROQ_API_KEY to your .env file.")
        print()
    else:
        print("Groq API key loaded from environment.")

    demo = build_ui()

    demo.launch()
