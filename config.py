import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists.
load_dotenv()


def get_api_key():
    """Return the OpenAI API key from the environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
        )
    return api_key


def get_model_name():
    """Return the model name to use for chat completions."""
    return os.getenv("MODEL_NAME", "gpt-4o-mini")
