# standard libs
import shlex
import argparse

# third party
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# local
from models.project import Project
from models.task import Task
from models.user import User
from utils.file_handler import load_data, save_data, parse_date, find_user, find_project, find_task

console = Console()


def print_help():
    help_text = Text()

    help_text.append(
        "Available commands\n", style="yellow")

    help_text.append("User:\n", style="yellow")
    help_text.append("  add-user", style="green")
    help_text.append(
        "     --name \"Name\" --email \"example@website.com\"\n", style="white")
    help_text.append("  list-users\n\n", style="green")

    help_text.append("Project:\n", style="yellow")
    help_text.append("  add-project", style="green")
    help_text.append(
        "   --user \"Name\" --title \"Title\" --description \"Description\" --due-date \"MM/DD/YYYY\"\n", style="white")
    help_text.append("  list-projects", style="green")
    help_text.append(" --user \"Name\"\n\n", style="white")

    help_text.append("Task:\n", style="yellow")
    help_text.append("  add-task", style="green")
    help_text.append(
        "      --project \"Name\" --title \"Title\" --assigned-to \"Name\"\n", style="white")
    help_text.append("  list-tasks", style="green")
    help_text.append("    --project \"Name\"\n", style="white")
    help_text.append("  complete-task", style="green")
    help_text.append(" --project \"Name\" --task \"Name\"\n", style="white")
    help_text.append("  update-task", style="green")
    help_text.append(
        "   --project \"Name\" --task \"Name\" --status \"incomplete\"|\"in progress\"|\"complete\"\n\n", style="white")

    help_text.append("Other:\n", style="yellow")
    help_text.append("  help", style="green")
    help_text.append("          show this panel\n", style="white")
    help_text.append("  exit", style="green")
    help_text.append("          quit the program\n\n", style="white")

    console.print(Panel(
        help_text,
        title="[bold blue]Project Management CLI[/bold blue]",
        subtitle="[dim]type a command to get started[/dim]",
        border_style="blue"
    ))


def setup_parser():
    parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers(dest="command")

    # help command
    subparsers.add_parser("help")

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

    # check if user already exists
    for user in data["users"]:
        if user["name"].lower() == args.name.lower():
            console.print(
                f"User '{args.name}' already exists.", style="bold red")
            return

    try:
        new_user = User(args.name, args.email)
    except (TypeError, ValueError) as error:
        console.print(f"Error: {error}", style="bold red")
        return

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

    table = Table(title="Users")
    table.add_column("Name", style="yellow")
    table.add_column("Email", style="blue")
    table.add_column("Projects", justify="right", style="green")

    for user in data["users"]:
        table.add_row(user["name"], user["email"], str(len(user["projects"])))

    console.print(table)


# project handlers

def handle_add_project(args):
    data = load_data()

    matched_user = find_user(data, args.user)
    if matched_user is None:
        console.print(f"User '{args.user}' not found.", style="bold red")
        return

    # check if project already exists under this user
    for project in matched_user["projects"]:
        if project["title"].lower() == args.title.lower():
            console.print(
                f"Project '{args.title}' already exists for '{args.user}'.", style="bold red")
            return

    # parse and validate the due date if one was provided
    due_date = None
    if args.due_date:
        due_date = parse_date(args.due_date)
        if due_date is None:
            console.print("Invalid date format. Use mm/dd/yyyy.",
                          style="bold red")
            return

    try:
        new_project = Project(args.title, args.description, due_date)
    except (TypeError, ValueError) as error:
        console.print(f"Error: {error}", style="bold red")
        return

    matched_user["projects"].append({
        "title": new_project.title,
        "description": new_project.description,
        "due_date": new_project.due_date.strftime("%m/%d/%Y") if new_project.due_date else None,
        "tasks": []
    })

    save_data(data)
    console.print(
        f"Project '{new_project.title}' added for '{args.user}'.", style="bold green")


def handle_list_projects(args):
    data = load_data()

    matched_user = find_user(data, args.user)
    if matched_user is None:
        console.print(f"User '{args.user}' not found.", style="bold red")
        return

    if not matched_user["projects"]:
        console.print(f"No projects found for '{args.user}'.", style="yellow")
        return

    table = Table(title=f"Projects for {matched_user['name']}")
    table.add_column("Title", style="yellow")
    table.add_column("Description", style="white")
    table.add_column("Due Date", style="blue")
    table.add_column("Tasks", justify="right", style="green")

    for project in matched_user["projects"]:
        table.add_row(
            project["title"],
            project["description"],
            project["due_date"] or "none",
            str(len(project["tasks"]))
        )

    console.print(table)


# task handlers

def handle_add_task(args):
    data = load_data()

    matched_project = find_project(data, args.project)
    if matched_project is None:
        console.print(f"Project '{args.project}' not found.", style="bold red")
        return

    # check if task already exists in this project
    for task in matched_project["tasks"]:
        if task["title"].lower() == args.title.lower():
            console.print(
                f"Task '{args.title}' already exists in '{args.project}'.", style="bold red")
            return

    if args.assigned_to:
        assigned_user = find_user(data, args.assigned_to)

        if assigned_user is None:
            console.print(
                f"User '{args.assigned_to}' not found.",
                style="bold red"
            )
            return

    try:
        new_task = Task(args.title, assigned_to=args.assigned_to)
    except (TypeError, ValueError) as error:
        console.print(f"Error: {error}", style="bold red")
        return

    matched_project["tasks"].append({
        "title": new_task.title,
        "status": new_task.status,
        "assigned_to": new_task.assigned_to
    })

    save_data(data)
    console.print(
        f"Task '{new_task.title}' added to '{args.project}'.", style="bold green")


def handle_list_tasks(args):
    data = load_data()

    matched_project = find_project(data, args.project)
    if matched_project is None:
        console.print(f"Project '{args.project}' not found.", style="bold red")
        return

    if not matched_project["tasks"]:
        console.print(f"No tasks found for '{args.project}'.", style="yellow")
        return

    table = Table(title=f"Tasks for {matched_project['title']}")
    table.add_column("Title", style="yellow")
    table.add_column("Status", style="blue")
    table.add_column("Assigned To", style="green")

    for task in matched_project["tasks"]:
        # color code status for quick visual scanning
        status = task["status"]
        if status == "complete":
            status_display = f"[green]{status}[/green]"
        elif status == "in progress":
            status_display = f"[yellow]{status}[/yellow]"
        else:
            status_display = f"[red]{status}[/red]"

        table.add_row(task["title"], status_display,
                      task["assigned_to"] or "unassigned")

    console.print(table)


def handle_complete_task(args):
    data = load_data()

    matched_project = find_project(data, args.project)
    if matched_project is None:
        console.print(f"Project '{args.project}' not found.", style="bold red")
        return

    matched_task = find_task(matched_project, args.task)
    if matched_task is None:
        console.print(
            f"Task '{args.task}' not found in '{args.project}'.", style="bold red")
        return

    matched_task["status"] = "complete"
    save_data(data)
    console.print(
        f"Task '{matched_task['title']}' marked as complete.", style="bold green")


def handle_update_task(args):
    data = load_data()

    matched_project = find_project(data, args.project)
    if matched_project is None:
        console.print(f"Project '{args.project}' not found.", style="bold red")
        return

    matched_task = find_task(matched_project, args.task)
    if matched_task is None:
        console.print(
            f"Task '{args.task}' not found in '{args.project}'.", style="bold red")
        return

    # reuse the task class setter to validate the status value
    try:
        temp_task = Task(matched_task["title"])
        temp_task.status = args.status
    except ValueError as error:
        console.print(f"Error: {error}", style="bold red")
        return

    matched_task["status"] = args.status
    save_data(data)
    console.print(
        f"Task '{matched_task['title']}' updated to '{args.status}'.", style="bold green")


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
    else:
        # covers both "help" and any unrecognized input that slips through
        print_help()


# main loop so it feels like a normal CLI instead of processing one command at a time
def main():
    parser = setup_parser()
    print_help()

    while True:
        try:
            raw_input = input("\n> ").strip()
        except KeyboardInterrupt:
            # handle ctrl+c gracefully
            console.print("\nExiting.", style="bold red")
            break

        if not raw_input:
            continue

        if raw_input.lower() in ("exit", "quit"):
            console.print("Goodbye.", style="bold blue")
            break

        # split input the same way a shell would so quoted strings stay together as one argument
        try:
            args_list = shlex.split(raw_input)
        except ValueError as error:
            console.print(f"Error parsing input: {error}", style="bold red")
            continue

        # argparse calls sys.exit() on bad args so we catch that here
        try:
            args = parser.parse_args(args_list)
        except SystemExit:
            continue

        if args.command is None:
            print_help()
            continue

        route(args)


if __name__ == "__main__":
    main()
