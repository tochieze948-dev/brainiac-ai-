import json
from pathlib import Path


class MemoryManager:
    def __init__(self, filename="personal_memory.json"):
        self.file = Path(filename)
        self.memories = self.load()

    def load(self):
        if self.file.exists():
            try:
                return json.loads(self.file.read_text())
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def remember(self, key, value):
        self.memories[key.lower()] = value
        self.save()
        return f"I'll remember that {key} is {value}."

    def recall(self, key):
        value = self.memories.get(key.lower())
        if value:
            return f"You told me that {key} is {value}."
        return f"I don't have a saved memory about {key}."

    def forget(self, key):
        if key.lower() in self.memories:
            del self.memories[key.lower()]
            self.save()
            return f"I've deleted my saved memory about {key}."
        return f"I couldn't find a saved memory about {key}."

    def save(self):
        self.file.write_text(
            json.dumps(self.memories, indent=4)
        )
