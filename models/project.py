from datetime import date
from .task import Task


class Project:
    def __init__(self, title, description, due_date=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Project title must be a string")

        value = value.strip()

        if not value:
            raise ValueError("Project title cannot be empty")

        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("Project description must be a string")

        value = value.strip()

        if not value:
            raise ValueError("Project description cannot be empty")

        self._description = value

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        if value is not None and not isinstance(value, date):
            raise TypeError(
                "Due date must be a date or left unspecified for no due date"
            )

        self._due_date = value

    def add_task(self, task):
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        self.tasks.append(task)

    def __str__(self):
        return self.title

    def __repr__(self):
        return (
            f"Project(title={self.title!r}, "
            f"description={self.description!r}, "
            f"due_date={self.due_date!r})"
        )
