import streamlit as st
from datetime import datetime
import autogen
from autogen import UserProxyAgent
from config.llm_config import code_llm_config, non_code_llm_config
from agents.base_agents import financial_assistant, research_assistant, writer
from agents.reviewer_agents import critic
from utils.review_utils import review_chats
import os

# Writing task for report generation
writing_tasks = [
    """
    You are a professional financial report writer. Based on the data provided by the analysts and researchers, write a structured financial report using this **exact Markdown format**:

    ```
    ## Overview
    (Summarize the objective of the report and the stocks analyzed.)

    ## Financial Ratios Table
    | Company | P/E | Forward P/E | Dividend Yield | Price-to-Book | Debt-to-Equity | ROE |
    |---------|-----|-------------|----------------|----------------|----------------|-----|
    |         |     |             |                |                |                |     |

    ## Explanation of Financial Metrics
    (Briefly explain what each ratio means and why it’s important.)

    ## Company-wise Financial Analysis
    ### [Company Name]
    - Analyze the ratios and what they reveal
    - Mention any financial highlights
    - Connect relevant news headlines

    (Repeat for each company.)

    ## Correlation and Risk Analysis
    (Summarize the correlation matrix, and discuss any market or sectoral risks.)

    ## Forward-Looking Scenario
    (Include 1–2 short scenarios per stock: growth expectations, risks, catalysts.)

    ```

    Do not modify the structure or introduce new sections.
    Only return your completed Markdown content, and nothing else.
    """
]

# Register nested reviewers
critic.register_nested_chats(review_chats, trigger=writer)

# Streamlit UI
st.title("Stock Analysis using LLM Agents")
assets = st.text_input("Assets you want to analyze (provide the tickers(e.g. 'NVDA' for Nvidia Corp.), comma-separated)?")
hit_button = st.button('Start analysis')

if hit_button and assets:
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Core tasks
    financial_tasks = [
        f"""You are a financial analysis agent. Analyze only these tickers: {assets}.

        1. Use yfinance to fetch:
        - Full company names for each ticker
        - 6 months of daily historical price data

        2. Normalize each stock's price (divide by first price) and use for correlation matrix only. Do not plot any chart.

        3. For each ticker, retrieve:
        - P/E Ratio
        - Forward P/E
        - Dividend Yield
        - Price-to-Book
        - Debt-to-Equity
        - Return on Equity (ROE)

        4. Calculate and return the correlation matrix of normalized prices

        5. Execute all relevant code. DO NOT return raw code blocks or snippets.

        Confirm at the end: "Financial metrics and correlation matrix computed"
        End your response with TERMINATE
        """,

        f"""You are a market research agent. For each ticker: {assets}, retrieve the latest company-specific financial news.

        1. Get the full company name using yfinance
        2. Use `requests` and `BeautifulSoup` to scrape 10 relevant headlines per company from Bing or Google News
        3. Validate relevance to each specific company (e.g., Apple Inc. vs Apple Bank)
        4. Format output as JSON:
        {{
            "Company Name": ["Headline 1", ..., "Headline 10"]
        }}
        5. DO NOT use APIs that require keys. DO NOT do sentiment analysis.

        Confirm that 10 headlines were retrieved per company
        End your response with TERMINATE
        """
    ]

    user_proxy_auto = UserProxyAgent(
        name="User_Proxy_Auto",
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "").strip().endswith("TERMINATE"),
        code_execution_config={
            "last_n_messages": 3,
            "work_dir": "coding",
            "use_docker": False,
        }
    )

    with st.spinner("Agents working on the analysis..."):
        chat_results = autogen.initiate_chats([
            {
                "sender": user_proxy_auto,
                "recipient": financial_assistant,
                "message": financial_tasks[0],
                "silent": False,
                "summary_method": "reflection_with_llm",
                "summary_args": {
                    "summary_prompt": (
                        "Return all extracted financial metrics and prices in a JSON format. "
                        "List full company names."
                    )
                },
                "clear_history": False,
                "carryover": "Ensure all values are real (not NaN or 0). Reply TERMINATE at the end."
            },
            {
                "sender": user_proxy_auto,
                "recipient": research_assistant,
                "message": financial_tasks[1],
                "silent": False,
                "summary_method": "reflection_with_llm",
                "summary_args": {
                    "summary_prompt": (
                        "Return the headlines in JSON format, grouped by full company name. "
                        "Do not return vague or irrelevant results. Be specific."
                    )
                },
                "clear_history": False,
                "carryover": "Reply TERMINATE after verifying all companies are covered with at least 10 headlines each."
            },
            {
                "sender": critic,
                "recipient": writer,
                "message": writing_tasks[0],
                "carryover": "Ensure all analysis from previous agents is reflected in the markdown report.",
                "max_turns": 2,
                "summary_method": "last_msg",
            }
        ])

    # Display the final report
    st.success("Report generation complete.")
    st.markdown(chat_results[-1].chat_history[-1]["content"])
