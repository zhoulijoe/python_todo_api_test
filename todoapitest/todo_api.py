#!/usr/bin/env python

import requests
from pprint import pprint
import argparse


SERVER_URL = "http://10.20.1.2/todo"


def get_token(username, password):
    """
    OAuth using username and password

    :param username: Username
    :param password: Password
    :return: Auth token
    """
    payload = {"grant_type": "password", "username": username, "password": password, "scope": "read"}
    r = requests.post(SERVER_URL + "/oauth/token", auth=("todo-client", "secret"), params=payload)
    token = r.json()["access_token"]

    return token


def with_auth(func):
    """
    Decorator for replacing username and password arguments with auth token as first argument of function

    :param func: Function to decorate
    :return: Function with username and password as first two positional arguments
    """
    def auth_wrapper(username, password, *args):
        token = get_token(username, password)
        return func(token, *args)

    return auth_wrapper


@with_auth
def query_tasks(token):
    """
    Get all tasks for a user

    :param token: Auth token
    :return: List of tasks
    """
    response = requests.get(SERVER_URL + "/task", headers=_gen_oauth_header(token))

    return response.json()


@with_auth
def query_task(token, id):
    """
    Get a single task based on id

    :param token: Auth token
    :param id: Task id
    :return: Task matching specified id
    """
    response = requests.get(SERVER_URL + "/task/" + id,
                                             headers=_gen_oauth_header(token))

    return response.json()


@with_auth
def add_task(token, description, complete):
    """
    Add a task with specified description and complete status

    :param token: Auth token
    :param description: Task description
    :param complete: Completion status
    :return: Newly added task
    """
    new_task = {"description": description, "complete": complete}

    add_request = requests.post(SERVER_URL + "/task", headers=_gen_oauth_header(token), json=new_task)

    return add_request.json()


@with_auth
def delete_task(token, id):
    """
    Delete a task based on specified id

    :param token: Auth token
    :param id: Task id
    :return: HTTP status code for the delete operation
    """
    response = requests.delete(SERVER_URL + "/task/" + id, headers=_gen_oauth_header(token))

    return response.status_code


@with_auth
def update_task(token, id, description, complete):
    """
    Update fields of a task based on specified id

    :param token: Auth token
    :param id: Task id
    :param description: Desired description
    :param complete: Desired completion status
    :return: Updated task
    """
    updated_task = {"description": description, "complete": complete}

    response = requests.put(SERVER_URL + "/task/" + id, headers=_gen_oauth_header(token), json=updated_task)

    return response.json()


def _gen_oauth_header(token):
    """
    Generate oauth header with token

    :param token: Auth token
    :return: Dictionary that contains header key-value pair for oauth
    """
    return {"Authorization": "Bearer " + token}


def run_test():
    """
    Main entry point for API test script that will parse command line arguments and execute corresponding test
    """
    parser = argparse.ArgumentParser(description="Test todo server API")

    parser.add_argument("operation", choices=["auth", "get_tasks"],
                        help="API operation to test")
    parser.add_argument("-u", "--username", required=True,
                        help="username")
    parser.add_argument("-p", "--password", required=True,
                        help="password")

    args = parser.parse_args()

    if args.operation == "auth":
        pprint(get_token(args.username, args.password))
    elif args.operation == "get_tasks":
        pprint(query_tasks(args.username, args.password))


if __name__ == "__main__":
    run_test()
