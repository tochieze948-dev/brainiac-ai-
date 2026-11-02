import json
from pathlib import Path


class TaskManager:
    """Save, view, and complete personal tasks."""

    def __init__(self, filename="tasks.json"):
        self.file = Path(filename)
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if self.file.exists():
            try:
                return json.loads(self.file.read_text())
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def save_tasks(self):
        self.file.write_text(json.dumps(self.tasks, indent=4))

    def add_task(self, description):
        task = {
            "description": description,
            "completed": False
        }
        self.tasks.append(task)
        self.save_tasks()
        return f"Task added: {description}"

    def show_tasks(self):
        if not self.tasks:
            return "You don't have any tasks yet."

        lines = ["Here are your tasks:"]

        for number, task in enumerate(self.tasks, start=1):
            status = "Done" if task["completed"] else "Pending"
            lines.append(
                f"{number}. [{status}] {task['description']}"
            )

        return "\n".join(lines)

    def complete_task(self, number):
        if number < 1 or number > len(self.tasks):
            return "That task number doesn't exist."

        task = self.tasks[number - 1]
        task["completed"] = True
        self.save_tasks()

        return f"Task completed: {task['description']}"
