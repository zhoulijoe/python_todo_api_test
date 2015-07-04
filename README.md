# python_todo_api_test

## Description

Api test against todo server

## Development Setup

    virtualenv venv
    source venv/bin/activate
    pip install -e .

## Run Test

    python todoapitest/todo_api.py -h

### Example

    # Get tasks for admin user
    python todoapitest/todo_api.py get_tasks -p admin -p admin
