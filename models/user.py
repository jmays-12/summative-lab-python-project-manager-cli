import re

from .project import Project


class User:
    _all = []

    EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.projects = []
        User._all.append(self)

    @classmethod
    def all(cls):
        return cls._all

    @classmethod
    def find_by_name(cls, name):
        return next(
            (user for user in cls._all if user.name.lower() == name.lower()),
            None
        )

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("User name must be a string")

        value = value.strip()

        if not value:
            raise ValueError("User name cannot be empty")

        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")

        value = value.strip()

        if not value:
            raise ValueError("Email cannot be empty")

        if not re.fullmatch(self.EMAIL_PATTERN, value):
            raise ValueError("Invalid email format")

        self._email = value

    def add_project(self, project):

        if not isinstance(project, Project):
            raise TypeError("Expected a Project instance")

        self.projects.append(project)

    def __str__(self):
        return f"{self.name} ({self.email})"

    def __repr__(self):
        return f"User(name={self.name!r}, email={self.email!r})"
