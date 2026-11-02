import json
import re
from pathlib import Path

from openai import OpenAI
from config import get_api_key, get_model_name
from memory_manager import MemoryManager
from tools import BrainiacTools
from task_manager import TaskManager

class BrainiacAI:
    """A personal AI assistant with memory and useful tools."""

    def __init__(self):
        self.model = get_model_name()
        self.memory_file = Path("memory.json")
        self.messages = self.load_memory()
        self.personal_memory = MemoryManager()
        self.tools = BrainiacTools()
        self.task_manager = TaskManager()
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
        self.memory_file.write_text(
            json.dumps(data, indent=4)
        )

    def save_exchange(self, user_message, reply):
        """Save a question and its answer."""
        self.messages.append({
            "role": "user",
            "content": user_message
        })
        self.messages.append({
            "role": "assistant",
            "content": reply
        })
        self.save_memory()

    def handle_memory_command(self, message):
        """Handle remember, recall, and forget requests."""

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

    def handle_calculation(self, message):
        """Recognize simple calculation requests."""

        number = r"\d[\d,]*(?:\.\d+)?"
        clean = message.lower().strip().rstrip("?!.")

        clean = re.sub(
            r"^(calculate|what is|what's)\s+",
            "",
            clean
        )

        percentage = re.fullmatch(
            rf"({number})\s*%\s*of\s*({number})",
            clean
        )

        if percentage:
            first = float(percentage.group(1).replace(",", ""))
            second = float(percentage.group(2).replace(",", ""))
            expression = f"({first} / 100) * {second}"
            return self.tools.calculate(expression)

        multiplication = re.fullmatch(
            rf"multiply\s+({number})\s+by\s+({number})",
            clean
        )

        if multiplication:
            first = multiplication.group(1).replace(",", "")
            second = multiplication.group(2).replace(",", "")
            return self.tools.calculate(f"{first} * {second}")

        operation = re.fullmatch(
            rf"({number})\s+(plus|minus|times|multiplied by|divided by|over)\s+({number})",
            clean
        )

        if operation:
            first = operation.group(1).replace(",", "")
            word = operation.group(2)
            second = operation.group(3).replace(",", "")

            symbols = {
                "plus": "+",
                "minus": "-",
                "times": "*",
                "multiplied by": "*",
                "divided by": "/",
                "over": "/"
            }

            expression = f"{first} {symbols[word]} {second}"
            return self.tools.calculate(expression)

        return None

   
    def handle_task_command(self, message):
        """Handle adding, viewing, and completing tasks."""

        message = message.strip()

        add_match = re.match(
            r"add task:\s*(.+)",
            message,
            re.IGNORECASE
        )

        if add_match:
            return self.task_manager.add_task(
                add_match.group(1).strip()
            )

        if message.lower() in ("show tasks", "show my tasks"):
            return self.task_manager.show_tasks()

        complete_match = re.match(
            r"complete task\s+(\d+)",
            message,
            re.IGNORECASE
        )

        if complete_match:
            return self.task_manager.complete_task(
                int(complete_match.group(1))
            )

        return None

    def ask(self, user_message: str) -> str:
        """Answer questions using memory, tools, or AI."""
        task_reply = self.handle_task_command(user_message)

        if task_reply is not None:
            self.save_exchange(user_message, task_reply)
            return task_reply
       
        memory_reply = self.handle_memory_command(user_message)

        if memory_reply is not None:
            self.save_exchange(user_message, memory_reply)
            return memory_reply

        calculation_reply = self.handle_calculation(user_message)

        if calculation_reply is not None:
            self.save_exchange(user_message, calculation_reply)
            return calculation_reply

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
                    "The user's saved personal facts are: "
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
