import pytest

from utils.file_handler import load_data, save_data
from models.task import Task
from models.project import Project
from models.user import User
from main import handle_add_user, handle_add_project, handle_add_task


# User tests

def test_user_creation():
    user = User("Alex Test", "alex@example.com")

    assert user.name == "Alex Test"
    assert user.email == "alex@example.com"


def test_user_rejects_invalid_email():
    with pytest.raises(ValueError):
        User("Alex Test", "not-an-email")


# Project tests

def test_project_creation():
    project = Project("CLI Tool", "A project manager")

    assert project.title == "CLI Tool"
    assert project.description == "A project manager"
    assert project.due_date is None


def test_project_rejects_empty_title():
    with pytest.raises(ValueError):
        Project("", "A project manager")


# Task tests

def test_task_defaults():
    task = Task("Implement add-task")

    assert task.status == "incomplete"
    assert task.assigned_to is None


def test_task_rejects_invalid_status():
    with pytest.raises(ValueError):
        Task("Implement add-task", status="done")


# File handling tests

def test_data_can_be_saved_and_loaded(tmp_path, monkeypatch):
    test_file = tmp_path / "test_data.json"
    monkeypatch.setattr("utils.file_handler.DATA_FILE", test_file)

    data = {
        "users": [],
        "projects": [],
        "tasks": []
    }

    save_data(data)
    loaded = load_data()

    assert loaded == data


def test_missing_data_file_returns_default_structure(tmp_path, monkeypatch):
    test_file = tmp_path / "missing.json"
    monkeypatch.setattr("utils.file_handler.DATA_FILE", test_file)

    loaded = load_data()

    assert loaded == {
        "users": []
    }


def test_add_user(tmp_path, monkeypatch, capsys):
    test_file = tmp_path / "test_data.json"
    monkeypatch.setattr("utils.file_handler.DATA_FILE", test_file)

    args = type("Args", (), {
        "name": "Alex Test",
        "email": "alex@example.com"
    })()

    handle_add_user(args)

    data = load_data()

    assert len(data["users"]) == 1
    assert data["users"][0]["name"] == "Alex Test"
    assert data["users"][0]["email"] == "alex@example.com"


def test_add_project(tmp_path, monkeypatch):
    test_file = tmp_path / "test_data.json"
    monkeypatch.setattr("utils.file_handler.DATA_FILE", test_file)

    save_data({
        "users": [{
            "name": "Alex Test",
            "email": "alex@example.com",
            "projects": []
        }]
    })

    args = type("Args", (), {
        "user": "Alex Test",
        "title": "CLI Tool",
        "description": "A project manager",
        "due_date": None
    })()

    handle_add_project(args)

    data = load_data()

    assert len(data["users"][0]["projects"]) == 1

    project = data["users"][0]["projects"][0]

    assert project["title"] == "CLI Tool"
    assert project["description"] == "A project manager"
    assert project["due_date"] is None
    assert project["tasks"] == []


def test_add_task(tmp_path, monkeypatch):
    test_file = tmp_path / "test_data.json"
    monkeypatch.setattr("utils.file_handler.DATA_FILE", test_file)

    save_data({
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
    })

    args = type("Args", (), {
        "project": "CLI Tool",
        "title": "Implement tests",
        "assigned_to": None
    })()

    handle_add_task(args)

    data = load_data()

    task = data["users"][0]["projects"][0]["tasks"][0]

    assert task["title"] == "Implement tests"
    assert task["status"] == "incomplete"
    assert task["assigned_to"] is None


def test_add_task_with_assignee(tmp_path, monkeypatch):
    test_file = tmp_path / "test_data.json"
    monkeypatch.setattr("utils.file_handler.DATA_FILE", test_file)

    save_data({
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
    })

    args = type("Args", (), {
        "project": "CLI Tool",
        "title": "Implement tests",
        "assigned_to": "Alex Test"
    })()

    handle_add_task(args)

    data = load_data()

    task = data["users"][0]["projects"][0]["tasks"][0]

    assert task["assigned_to"] == "Alex Test"


def test_add_duplicate_user_is_rejected(tmp_path, monkeypatch):
    test_file = tmp_path / "test_data.json"
    monkeypatch.setattr("utils.file_handler.DATA_FILE", test_file)

    save_data({
        "users": [{
            "name": "Alex Test",
            "email": "alex@example.com",
            "projects": []
        }]
    })

    args = type("Args", (), {
        "name": "alex test",
        "email": "another@example.com"
    })()

    handle_add_user(args)

    data = load_data()

    assert len(data["users"]) == 1
    assert data["users"][0]["email"] == "alex@example.com"


def test_add_task_rejects_unknown_assignee(tmp_path, monkeypatch):
    test_file = tmp_path / "test_data.json"
    monkeypatch.setattr("utils.file_handler.DATA_FILE", test_file)

    save_data({
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
    })

    args = type("Args", (), {
        "project": "CLI Tool",
        "title": "Implement tests",
        "assigned_to": "Nobody"
    })()

    handle_add_task(args)

    data = load_data()

    assert data["users"][0]["projects"][0]["tasks"] == []
