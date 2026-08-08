import re
from .project import Project


class User:
    _all = []
    # basic regex pattern to validate email addresses
    EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.projects = []
        User._all.append(self)

    @classmethod
    def all(cls):
        return cls.all

    @classmethod
    def find_by_name(cls, name):
        return next((user for user in cls._all if user.name == name), None)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # User name can only be a string and must not be empty
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
        # make sure input email is a string before doing .strip()
        if not isinstance(value, str):
            raise TypeError("Email must be a string")

        value = value.strip()

        if not value:
            raise ValueError("Email cannot be empty")
        # validate email address at least has email address format
        if not re.fullmatch(self.EMAIL_PATTERN, value):
            raise ValueError("Invalid email format")

        self._email = value

    def add_project(self, project):
        if not hasattr(project, "title") or not hasattr(project, "description"):
            raise TypeError("Expected a Project instance")
        self.projects.append(project)
