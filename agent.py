from openai import OpenAI

from config import get_api_key, get_model_name


class BrainiacAI:
    """A simple chat agent that talks to an AI API."""

    def __init__(self):
        self.client = OpenAI(api_key=get_api_key())
        self.model = get_model_name()

    def ask(self, user_message: str) -> str:
        """Send a user message to the AI model and return the reply."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Brainiac AI, a friendly and helpful personal assistant. "
                        "Answer clearly, simply, and kindly. Help with everyday tasks, "
                        "questions, and general problem-solving."
                    ),
                },
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        return response.choices[0].message.content.strip()
