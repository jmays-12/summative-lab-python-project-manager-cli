# standard libs
import shlex
import argparse

# third party
from rich.console import Console
from rich.table import Table

# local
from models.project import Project
from models.task import Task
from models.user import User
from utils.file_handler import load_data, save_data

console = Console()


def setup_parser():
    parser = argparse.ArgumentParser(description="Project Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    # user commands
    add_user_parser = subparsers.add_parser("add-user")
    add_user_parser.add_argument("--name", required=True)
    add_user_parser.add_argument("--email", required=True)

    subparsers.add_parser("list-users")

    # project commands
    add_project_parser = subparsers.add_parser("add-project")
    add_project_parser.add_argument("--user", required=True)
    add_project_parser.add_argument("--title", required=True)
    add_project_parser.add_argument("--description", required=True)
    add_project_parser.add_argument("--due-date", default=None)

    list_projects_parser = subparsers.add_parser("list-projects")
    list_projects_parser.add_argument("--user", required=True)

    # task commands
    add_task_parser = subparsers.add_parser("add-task")
    add_task_parser.add_argument("--project", required=True)
    add_task_parser.add_argument("--title", required=True)
    add_task_parser.add_argument("--assigned-to", default=None)

    list_tasks_parser = subparsers.add_parser("list-tasks")
    list_tasks_parser.add_argument("--project", required=True)

    complete_task_parser = subparsers.add_parser("complete-task")
    complete_task_parser.add_argument("--project", required=True)
    complete_task_parser.add_argument("--task", required=True)

    update_task_parser = subparsers.add_parser("update-task")
    update_task_parser.add_argument("--project", required=True)
    update_task_parser.add_argument("--task", required=True)
    update_task_parser.add_argument("--status", required=True)

    return parser


# user handlers

def handle_add_user(args):
    data = load_data()

    for user in data["users"]:
        if user["name"].lower() == args.name.lower():
            console.print(
                f"User '{args.name}' already exists.", style="bold red")
            return

    new_user = User(args.name, args.email)

    data["users"].append({
        "name": new_user.name,
        "email": new_user.email,
        "projects": []
    })

    save_data(data)
    console.print(
        f"User '{new_user.name}' added successfully.", style="bold green")


def handle_list_users():
    data = load_data()

    if not data["users"]:
        console.print("No users found.", style="yellow")
        return

    for user in data["users"]:
        console.print(f"{user['name']} - {user['email']}")


# project handlers

def handle_add_project(args):
    data = load_data()

    matched_user = None
    for user in data["users"]:
        if user["name"].lower() == args.user.lower():
            matched_user = user
            break

    if matched_user is None:
        console.print(f"User '{args.user}' not found.", style="bold red")
        return

    matched_user["projects"].append({
        "title": args.title,
        "description": args.description,
        "due_date": args.due_date,
        "tasks": []
    })

    save_data(data)
    console.print(
        f"Project '{args.title}' added for '{args.user}'.", style="bold green")


def handle_list_projects(args):
    pass


# task handlers

def handle_add_task(args):
    pass


def handle_list_tasks(args):
    pass


def handle_complete_task(args):
    pass


def handle_update_task(args):
    pass


# routing

def route(args):
    if args.command == "add-user":
        handle_add_user(args)
    elif args.command == "list-users":
        handle_list_users()
    elif args.command == "add-project":
        handle_add_project(args)
    elif args.command == "list-projects":
        handle_list_projects(args)
    elif args.command == "add-task":
        handle_add_task(args)
    elif args.command == "list-tasks":
        handle_list_tasks(args)
    elif args.command == "complete-task":
        handle_complete_task(args)
    elif args.command == "update-task":
        handle_update_task(args)


def main():
    parser = setup_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    route(args)


if __name__ == "__main__":
    main()
