import requests
import pprint


SERVER_URL = "http://10.20.1.2/todo"


def get_token(username, password):
    payload = {"grant_type": "password", "username": username, "password": password, "scope": "read"}
    r = requests.post(SERVER_URL + "/oauth/token", auth=("todo-client", "secret"), params=payload)
    token = r.json()["access_token"]

    return token


def gen_quth_header(token):
    return {"Authorization": "Bearer " + token}


def query_tasks(token):
    query_task_request = requests.get(SERVER_URL + "/task", headers=gen_quth_header(token))
    pprint.pprint(query_task_request.json())


def query_task(token, id):
    query_single_task_request = requests.get(SERVER_URL + "/task/" + id,
                                             headers=gen_quth_header(token))
    pprint.pprint(query_single_task_request.json())


def add_task(token, description, complete):
    new_task = {"description": description, "complete": complete}

    add_request = requests.post(SERVER_URL + "/task", headers=gen_quth_header(token), json=new_task)

    pprint.pprint(add_request.json())


def delete_task(token, id):
    delete_request = requests.delete(SERVER_URL + "/task/" + id, headers=gen_quth_header(token))

    pprint.pprint(delete_request.status_code)


def update_task(token, id, description, complete):
    updated_task = {"description": description, "complete": complete}

    update_request = requests.put(SERVER_URL + "/task/" + id, headers=gen_quth_header(token), json=updated_task)

    pprint.pprint(update_request.json())
