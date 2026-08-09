import pytest

from utils.file_handler import load_data, save_data
from models.task import Task
from models.project import Project
from models.user import User
from main import (
    handle_add_user,
    handle_add_project,
    handle_add_task,
    handle_complete_task,
    handle_update_task,
)


# small helper so the cli tests don't repeat the same setup everywhere

def make_test_data():
    return {
        "users": [{
            "name": "Alex Test",
            "email": "alex@example.com",
            "projects": [{
                "title": "CLI Tool",
                "description": "A project manager",
                "due_date": None,
                "tasks": []
            }]
        }]
    }


def make_args(**kwargs):
    # makes fake argparse arguments without needing to run the whole cli
    return type("Args", (), kwargs)()


def use_test_file(tmp_path, monkeypatch):
    # keep tests from touching the real app data file
    test_file = tmp_path / "test_data.json"
    monkeypatch.setattr("utils.file_handler.DATA_FILE", test_file)
    return test_file


# User tests

def test_user_creation():
    user = User("Alex Test", "alex@example.com")

    assert user.name == "Alex Test"
    assert user.email == "alex@example.com"


def test_user_rejects_invalid_email():
    with pytest.raises(ValueError):
        User("Alex Test", "not-an-email")


def test_user_can_add_project():
    user = User("Alex Test", "alex@example.com")
    project = Project("CLI Tool", "A project manager")

    user.add_project(project)

    assert project in user.projects


# Project tests

def test_project_creation():
    project = Project("CLI Tool", "A project manager")

    assert project.title == "CLI Tool"
    assert project.description == "A project manager"
    assert project.due_date is None


def test_project_rejects_empty_title():
    with pytest.raises(ValueError):
        Project("", "A project manager")


def test_project_can_add_task():
    project = Project("CLI Tool", "A project manager")
    task = Task("Implement tests")

    project.add_task(task)

    assert task in project.tasks

# Task tests


def test_task_defaults():
    task = Task("Implement add-task")

    assert task.status == "incomplete"
    assert task.assigned_to is None


def test_task_rejects_invalid_status():
    with pytest.raises(ValueError):
        Task("Implement add-task", status="done")


def test_task_string_representations():
    task = Task(
        "Implement tests",
        status="in progress",
        assigned_to="Alex Test"
    )

    assert str(task) == "Implement tests [in progress]"
    assert repr(task) == (
        "Task(title='Implement tests', "
        "status='in progress', "
        "assigned_to='Alex Test')"
    )


# File handling tests

def test_data_can_be_saved_and_loaded(tmp_path, monkeypatch):
    use_test_file(tmp_path, monkeypatch)

    data = {
        "users": [],
        "projects": [],
        "tasks": []
    }

    save_data(data)
    loaded = load_data()

    assert loaded == data


def test_missing_data_file_returns_default_structure(tmp_path, monkeypatch):
    use_test_file(tmp_path, monkeypatch)

    loaded = load_data()

    assert loaded == {
        "users": []
    }


def test_malformed_data_file_returns_default_structure(tmp_path, monkeypatch):
    test_file = use_test_file(tmp_path, monkeypatch)

    # write something that definitely isn't valid json
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text(
        "{this is not valid json",
        encoding="utf-8"
    )

    loaded = load_data()

    assert loaded == {
        "users": []
    }


# CLI tests

def test_add_user(tmp_path, monkeypatch):
    use_test_file(tmp_path, monkeypatch)

    args = make_args(
        name="Alex Test",
        email="alex@example.com"
    )

    handle_add_user(args)

    data = load_data()

    assert len(data["users"]) == 1
    assert data["users"][0]["name"] == "Alex Test"
    assert data["users"][0]["email"] == "alex@example.com"


def test_add_duplicate_user_is_rejected(tmp_path, monkeypatch):
    use_test_file(tmp_path, monkeypatch)

    save_data({
        "users": [{
            "name": "Alex Test",
            "email": "alex@example.com",
            "projects": []
        }]
    })

    args = make_args(
        name="alex test",
        email="another@example.com"
    )

    handle_add_user(args)

    data = load_data()

    # the second user shouldn't have been added
    assert len(data["users"]) == 1
    assert data["users"][0]["email"] == "alex@example.com"


def test_add_project(tmp_path, monkeypatch):
    use_test_file(tmp_path, monkeypatch)

    save_data({
        "users": [{
            "name": "Alex Test",
            "email": "alex@example.com",
            "projects": []
        }]
    })

    args = make_args(
        user="Alex Test",
        title="CLI Tool",
        description="A project manager",
        due_date=None
    )

    handle_add_project(args)

    data = load_data()
    project = data["users"][0]["projects"][0]

    assert len(data["users"][0]["projects"]) == 1
    assert project["title"] == "CLI Tool"
    assert project["description"] == "A project manager"
    assert project["due_date"] is None
    assert project["tasks"] == []


def test_add_task(tmp_path, monkeypatch):
    use_test_file(tmp_path, monkeypatch)
    save_data(make_test_data())

    args = make_args(
        project="CLI Tool",
        title="Implement tests",
        assigned_to=None
    )

    handle_add_task(args)

    data = load_data()
    task = data["users"][0]["projects"][0]["tasks"][0]

    assert task["title"] == "Implement tests"
    assert task["status"] == "incomplete"
    assert task["assigned_to"] is None


def test_add_task_with_assignee(tmp_path, monkeypatch):
    use_test_file(tmp_path, monkeypatch)
    save_data(make_test_data())

    args = make_args(
        project="CLI Tool",
        title="Implement tests",
        assigned_to="Alex Test"
    )

    handle_add_task(args)

    data = load_data()
    task = data["users"][0]["projects"][0]["tasks"][0]

    assert task["assigned_to"] == "Alex Test"


def test_complete_task(tmp_path, monkeypatch):
    use_test_file(tmp_path, monkeypatch)

    data = make_test_data()
    data["users"][0]["projects"][0]["tasks"].append({
        "title": "Implement tests",
        "status": "incomplete",
        "assigned_to": None
    })
    save_data(data)

    args = make_args(
        project="CLI Tool",
        task="Implement tests"
    )

    handle_complete_task(args)

    data = load_data()

    assert (
        data["users"][0]["projects"][0]["tasks"][0]["status"]
        == "complete"
    )


def test_update_task(tmp_path, monkeypatch):
    use_test_file(tmp_path, monkeypatch)

    data = make_test_data()
    data["users"][0]["projects"][0]["tasks"].append({
        "title": "Implement tests",
        "status": "incomplete",
        "assigned_to": None
    })
    save_data(data)

    args = make_args(
        project="CLI Tool",
        task="Implement tests",
        status="in progress"
    )

    handle_update_task(args)

    data = load_data()

    assert (
        data["users"][0]["projects"][0]["tasks"][0]["status"]
        == "in progress"
    )


def test_update_task_rejects_invalid_status(tmp_path, monkeypatch):
    use_test_file(tmp_path, monkeypatch)

    data = make_test_data()
    data["users"][0]["projects"][0]["tasks"].append({
        "title": "Implement tests",
        "status": "incomplete",
        "assigned_to": None
    })
    save_data(data)

    args = make_args(
        project="CLI Tool",
        task="Implement tests",
        status="done"
    )

    handle_update_task(args)

    data = load_data()

    # invalid status should leave the original value alone
    assert (
        data["users"][0]["projects"][0]["tasks"][0]["status"]
        == "incomplete"
    )
