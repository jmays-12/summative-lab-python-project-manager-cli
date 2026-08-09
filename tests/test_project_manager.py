from utils.file_handler import load_data, save_data
from models.task import Task
from models.project import Project
from models.user import User
import pytest


# User tests

def test_user_creation():
    user = User("Alex Jones", "alex@example.com")

    assert user.name == "Alex Jones"
    assert user.email == "alex@example.com"


def test_user_rejects_invalid_email():
    with pytest.raises(ValueError):
        User("Alex Jones", "not-an-email")


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
