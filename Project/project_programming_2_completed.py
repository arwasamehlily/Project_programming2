
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List


# SRP: Single Responsibility Principle
class Task:
    """Class for adding and updating task status."""
    def __init__(self, title, priority="Medium"):
        self.title = title
        self.completed = False
        self.priority = priority
        self.created_at = datetime.now()

    def update_status(self, status: bool):
        """Update task status."""
        self.completed = status

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"Task: {self.title}, Priority: {self.priority}, Status: {status}"


class Reminder:
    """Class for sending reminders."""
    def __init__(self, reminder_type: str):
        self.reminder_type = reminder_type  # Type of reminder (e.g., SMS, Email)

    def send_reminder(self, task: Task):
        """Send a reminder for the task."""
        print(f"Reminder sent for task: {task.title} via {self.reminder_type}")


# OCP: Open/Closed Principle
class PriorityTask(Task):
    """Class for setting task priorities."""
    def __init__(self, title, priority="High"):
        super().__init__(title, priority)


class RecurringTask(Task):
    """Class for recurring tasks."""
    def __init__(self, title, recurrence: str):
        super().__init__(title)
        self.recurrence = recurrence

    def __str__(self):
        return f"{super().__str__()}, Recurrence: {self.recurrence}"


# LSP: Liskov Substitution Principle
class SimpleTask(Task):
    pass


class AdvancedTask(Task):
    def __init__(self, title, priority="Low", extra_notes=""):
        super().__init__(title, priority)
        self.extra_notes = extra_notes

    def __str__(self):
        return f"{super().__str__()}, Notes: {self.extra_notes}"


# ISP: Interface Segregation Principle
class ReminderInterface(ABC):
    """Interface for reminders."""
    @abstractmethod
    def set_reminder(self, task: Task, reminder_text: str):
        pass


class EmailReminder(ReminderInterface):
    def set_reminder(self, task: Task, reminder_text: str):
        print(f"Email reminder for task '{task.title}': {reminder_text}")


class SMSReminder(ReminderInterface):
    def set_reminder(self, task: Task, reminder_text: str):
        print(f"SMS reminder for task '{task.title}': {reminder_text}")


# DIP: Dependency Inversion Principle
class ReminderManager:
    """Handles reminders using ReminderInterface."""
    def __init__(self, reminder_service: ReminderInterface):
        self.reminder_service = reminder_service

    def send_reminder(self, task: Task, reminder_text: str):
        self.reminder_service.set_reminder(task, reminder_text)


# To-Do List Application
class ToDoApp:
    """Main application to manage tasks."""
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)
        print(f"Task added: {task}")

    def display_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return
        print("Tasks List:")
        for task in self.tasks:
            print(task)

    def update_task_status(self, title: str, status: bool):
        task = self.find_task(title)
        if task:
            task.update_status(status)
            print(f"Task '{title}' status updated to: {'Completed' if status else 'Pending'}")

    def find_task(self, title: str) -> Task:
        for task in self.tasks:
            if task.title == title:
                return task
        print(f"Task '{title}' not found.")
        return None


if __name__ == "__main__":
    app = ToDoApp()

    # Adding tasks
    task1 = Task("Buy groceries")
    task2 = PriorityTask("Complete project", priority="High")
    task3 = RecurringTask("Workout", recurrence="Daily")
    task4 = AdvancedTask("Plan vacation", priority="Medium", extra_notes="Include family preferences.")

    app.add_task(task1)
    app.add_task(task2)
    app.add_task(task3)
    app.add_task(task4)

    # Display tasks
    app.display_tasks()

    # Update task status
    app.update_task_status("Buy groceries", True)

    # Send reminders
    email_reminder = EmailReminder()
    sms_reminder = SMSReminder()

    email_manager = ReminderManager(email_reminder)
    sms_manager = ReminderManager(sms_reminder)

    email_manager.send_reminder(task2, "Deadline is tomorrow!")
    sms_manager.send_reminder(task3, "Don't forget your workout!")
