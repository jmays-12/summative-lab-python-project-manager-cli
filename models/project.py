class Project:
    def __init__(self, title, description, due_date=None):
        self.title = title
        self.description = description
        if due_date:
            self.due_date = due_date
