class Task:

    VALID_STATUSES = ("incomplete", "in progress", "complete")

    def __init__(self, title, status="incomplete", assigned_to=None):
        self.title = title
        self.status = status
        self.assigned_to = assigned_to

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # title can only be assigned to a string, and must not be empty
        if not isinstance(value, str):
            raise TypeError("Title must be a string")

        if not value.strip():
            raise ValueError("Title cannot be empty")

        self._title = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.VALID_STATUSES:
            # format list of valid statuses instead of hard coding in case it changes later
            valid = ", ".join(self.VALID_STATUSES)
            raise ValueError(
                f"Invalid task status. Valid statuses are: {valid}"
            )

        self._status = value

    @property
    def assigned_to(self):
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, assignee):
        # allow task to be assigned to no one
        if assignee is None:
            self._assigned_to = None
        # allow task to be assigned to user ID
        elif isinstance(assignee, int) and assignee > 0:
            self._assigned_to = assignee
        else:
            raise TypeError(
                "User ID must be a positive integer or left empty.")
