import os
from dotenv import load_dotenv

load_dotenv()

# Coding agents' LLM config
code_llm_config = {
    "config_list": [{
        "model": os.getenv("CODE_MODEL"),
        "api_key": os.getenv("CODE_API_KEY"),
        "base_url": "https://api.groq.com/openai/v1",
    }]
}

# Non-coding agents' LLM config
non_code_llm_config = {
    "config_list": [{
        "model": os.getenv("NON_CODE_MODEL"),
        "api_key": os.getenv("NON_CODE_API_KEY"),
        "base_url": "https://api.groq.com/openai/v1",
    }]
}
