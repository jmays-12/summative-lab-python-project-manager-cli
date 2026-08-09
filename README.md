# Project Manager CLI

A Python-based CLI (command-line interface) project management tool.

Add any number of tasks to a project, and any number of projects to a user.

## Features

* Tracks users, projects, and tasks.
* Persistent data storage using JSON.
* Interactive CLI with a focus on readability and ease of use.
* Input validation for user names, email addresses, task statuses, project information, and due dates.
* Tasks can be assigned to users.
* Create, list, complete, and update tasks.
* Create and list users and projects.

## Requirements

* Python 3
* rich
* pytest

## Running

In the terminal, run:

```bash
python main.py
```

The CLI will display the available commands when it starts.

## Testing

Run the test suite with:

```bash
pytest
```
