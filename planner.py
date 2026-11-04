import json
from pathlib import Path
from datetime import date


class DailyPlanner:
    """Organize daily tasks by category, date, and priority."""

    def __init__(self, filename="planner.json"):
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

    def add_task(self, description, category, due_date, priority):
        task = {
            "description": description,
            "category": category,
            "due_date": due_date,
            "priority": priority,
            "completed": False
        }

        self.tasks.append(task)
        self.save_tasks()

        return f"Added to your planner: {description}"

    def show_today(self):
        today = date.today().isoformat()

        today_tasks = [
            task for task in self.tasks
            if task["due_date"] == today
        ]

        if not today_tasks:
            return "You have no tasks scheduled for today."

        lines = ["Here is your plan for today:"]

        for number, task in enumerate(today_tasks, start=1):
            status = "Done" if task["completed"] else "Pending"

            lines.append(
                f"{number}. [{status}] {task['description']}"
                f" | {task['category']}"
                f" | Priority: {task['priority']}"
            )

        return "\n".join(lines)
    def show_all(self):
        if not self.tasks:
            return "Your planner is empty."

        lines = ["Here are all your planned tasks:"]

        for number, task in enumerate(self.tasks, start=1):
            status = "Done" if task["completed"] else "Pending"

            lines.append(
                f"{number}. [{status}] {task['description']}"
                f" | {task['category']}"
                f" | Due: {task['due_date']}"
                f" | Priority: {task['priority']}"
            )

        return "\n".join(lines)

    def complete_task(self, number):
        if number < 1 or number > len(self.tasks):
            return "That task number doesn't exist."

        task = self.tasks[number - 1]
        task["completed"] = True
        self.save_tasks()

        return f"Completed: {task['description']}"
