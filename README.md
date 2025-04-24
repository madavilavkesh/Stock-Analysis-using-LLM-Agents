# Stock Analysis using LLM Agents

This project leverages **Large Language Models (LLMs)** and **autogen agents** for automated stock analysis. It performs financial data retrieval, news scraping, and generates comprehensive financial reports using AI agents. The entire process is orchestrated through a **Streamlit** web interface for easy interaction.

## Features

- **Multi-Agent System:** The project utilizes several LLM agents to perform distinct tasks:
  - **Financial Assistant:** Retrieves stock data, computes financial ratios, and generates a correlation matrix.
  - **Research Assistant:** Scrapes the latest news headlines for each stock.
  - **Writer:** Converts the analysis into a structured financial report in Markdown format.
  - **Reviewer Agents:** Critic, Legal, and Consistency reviewers ensure the quality and accuracy of the final report.

- **Web Interface:** Built using Streamlit, the web interface allows users to input stock tickers and start the analysis.

- **Automated Report Generation:** Once the analysis is complete, a financial report is generated based on a predefined Markdown format, summarizing the financial metrics and relevant news.

## Tech Stack

- **Backend:** Python
- **Libraries:** 
  - **Streamlit** (for web interface)
  - **autogen** (for multi-agent orchestration)
  - **yfinance** (for stock data retrieval)
  - **BeautifulSoup** and **requests** (for news scraping)
- **APIs:** Groq API (for LLM model execution)
- **Environment Variables:** `.env` file for managing API keys securely
- **Other Tools:** Docker, JSON, Markdown

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-analysis-llm-agents.git
cd stock-analysis-llm-agents
```

### 2. Install dependencies:
Make sure you have Python 3.8+ installed. Create a virtual environment and install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables:
Create a `.env` file in the root directory and add your API keys:
```env
CODE_API_KEY=your_code_api_key
CODE_MODEL=your_code_model_name
NON_CODE_API_KEY=your_non_code_api_key
NON_CODE_MODEL=your_non_code_model_name
```

### 4. Run the application:
Launch the app using Streamlit:
```bash
streamlit run app.py
```
Visit `http://localhost:8501` in your browser to interact with the app.

## Usage

1. **Enter Stock Tickers:** Input the stock tickers you want to analyze (e.g., `NVDA` for Nvidia) into the text input box.
2. **Start Analysis:** Click on the **Start analysis** button to trigger the agents.
3. **Review the Report:** Once the analysis is complete, the report will be displayed in the UI, summarizing the financial metrics and stock data.

## File Structure

- `app.py`: Main Streamlit app that handles user input and displays results.
- `agents/`: Contains the agent definitions for various tasks (financial analysis, news scraping, report writing).
- `config/`: Holds configuration files, including LLM model details.
- `requirements.txt`: Lists the required Python packages.
- `.env`: Stores environment variables such as API keys.
- `utils/`: Contains utility functions for reviews and agent management.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
