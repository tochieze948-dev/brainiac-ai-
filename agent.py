import json
import re
from pathlib import Path

from openai import OpenAI
from config import get_api_key, get_model_name
from memory_manager import MemoryManager


class BrainiacAI:
    """A personal AI assistant with conversation and personal memory."""

    def __init__(self):
        self.model = get_model_name()
        self.memory_file = Path("memory.json")
        self.messages = self.load_memory()
        self.personal_memory = MemoryManager()

        self.client = OpenAI(
            api_key=get_api_key(),
            base_url="https://api.groq.com/openai/v1"
        )

    def load_memory(self):
        """Load previous conversations."""
        try:
            if self.memory_file.exists():
                data = json.loads(self.memory_file.read_text())
                return data.get("messages", [])
        except (json.JSONDecodeError, OSError):
            print("Starting with fresh memory.")

        return []

    def save_memory(self):
        """Save conversations to the phone."""
        data = {"messages": self.messages}
        self.memory_file.write_text(json.dumps(data, indent=4))

    def handle_memory_command(self, message):
        """Handle simple remember, recall, and forget requests."""

        remember_match = re.search(
            r"remember that (.+?) is (.+?)[.!?]*$",
            message,
            re.IGNORECASE
        )

        if remember_match:
            key = remember_match.group(1).strip()
            value = remember_match.group(2).strip()
            key = re.sub(r"^my\s+", "", key, flags=re.IGNORECASE)

            return self.personal_memory.remember(key, value)

        recall_match = re.search(
            r"(?:what is|what's) my (.+?)[?!.]*$",
            message,
            re.IGNORECASE
        )

        if recall_match:
            key = recall_match.group(1).strip()
            return self.personal_memory.recall(key)

        forget_match = re.search(
            r"forget my (.+?)[?!.]*$",
            message,
            re.IGNORECASE
        )

        if forget_match:
            key = forget_match.group(1).strip()
            return self.personal_memory.forget(key)

        return None

    def ask(self, user_message: str) -> str:
        """Answer questions and remember useful information."""

        memory_reply = self.handle_memory_command(user_message)

        if memory_reply is not None:
            self.messages.append({
                "role": "user",
                "content": user_message
            })
            self.messages.append({
                "role": "assistant",
                "content": memory_reply
            })
            self.save_memory()
            return memory_reply

        self.messages.append({
            "role": "user",
            "content": user_message
        })

        saved_facts = json.dumps(
            self.personal_memory.memories,
            indent=2
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are Brainiac AI, a friendly personal assistant. "
                    "Answer clearly, simply, and helpfully. "
                    "Here are the user's saved personal facts: "
                    + saved_facts
                )
            }
        ] + self.messages

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )

            reply = response.choices[0].message.content or ""

            self.messages.append({
                "role": "assistant",
                "content": reply
            })

            self.save_memory()
            return reply

        except Exception:
            self.messages.pop()
            raise
