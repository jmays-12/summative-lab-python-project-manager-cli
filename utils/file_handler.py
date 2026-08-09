import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "data.json"


def load_data():
    if not DATA_FILE.exists():
        return {"users": []}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print("Warning: data file was malformed, starting fresh.")
            return {"users": []}


def save_data(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def parse_date(date_string):
    # accepts mm/dd/yyyy only
    try:
        return datetime.strptime(date_string, "%m/%d/%Y").date()
    except ValueError:
        return None


def find_user(data, name):
    # search all users for a matching name
    for user in data["users"]:
        if user["name"].lower() == name.lower():
            return user
    return None


def find_project(data, project_title):
    # search all users for a project matching the given title
    for user in data["users"]:
        for project in user["projects"]:
            if project["title"].lower() == project_title.lower():
                return project
    return None


def find_task(project, task_title):
    # search a project for a task matching the given title
    for task in project["tasks"]:
        if task["title"].lower() == task_title.lower():
            return task
    return None
