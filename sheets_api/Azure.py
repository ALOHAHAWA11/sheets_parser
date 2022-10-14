import requests
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication


def connect_to_azure():
    global personal_access_token
    personal_access_token = 'oaobzcc2udgdcmtlnncd75xumdqgytiqfe7jft62bp7hlzqpinwq'
    organization_url = 'https://dev.azure.com/nikitau'
    credentials = BasicAuthentication('', personal_access_token)
    Connection(base_url=organization_url, creds=credentials)


def create_issue(header, url='https://dev.azure.com/nikitau/destination/_apis/wit/workitems/$Issue?api-version=6.0'):
    global issue_id
    data = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": header.company,
        },
    ]
    req = requests.post(url, json=data, headers={'Content-Type': 'application/json-patch+json'},
                        auth=('', personal_access_token)).json()
    issue_id = req['id']
    return issue_id


def create_subtask(task, url):
    for subtask in task.sub_tasks:
        data = [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": subtask.task_name,
            },
        ]
        if subtask.description:
            data.append(
                {
                    "op": "add",
                    "path": "/fields/System.Description",
                    "value": subtask.description,
                }
            )
        req = requests.post(url, json=data, headers={'Content-Type': 'application/json-patch+json'},
                            auth=('', personal_access_token)).json()
        # print(req)
        task_id = req['id']
        bound_tasks_and_issue(issue_id, task_id)


def create_task(task, url='https://dev.azure.com/nikitau/destination/_apis/wit/workitems/$Task?api-version=6.0'):
    data = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": '== ' + task.task_name.upper() + ' ==',
        }
    ]
    if task.description:
        data.append(
            {
                "op": "add",
                "path": "System.Description",
                "value": task.description,
            }
        )
    req = requests.post(url, json=data, headers={'Content-Type': 'application/json-patch+json'},
                        auth=('', personal_access_token)).json()
    # print(req)
    task_id = req['id']
    if task.sub_tasks:
        create_subtask(task, url)
    return task_id


def bound_tasks_and_issue(issue_id, task_id):
    url = 'https://dev.azure.com/nikitau/destination/_apis/wit/workitems/{0}?api-version=6.1-preview.3'.format(task_id)
    data = [
        {
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": "https://dev.azure.com/nikitau/destination/_apis/wit/workItems/{0}".format(issue_id),
                "attributes": {
                    "isLocked": False,
                    "name": "Parent",

                }
            },
        }

    ]
    return requests.patch(url, json=data, headers={'Content-Type': 'application/json-patch+json'},
                          auth=('', personal_access_token)).json()


def send_to_azure(header, tasks):
    connect_to_azure()
    issue_id = create_issue(header)
    for task in tasks:
        task = create_task(task)
        bound = bound_tasks_and_issue(issue_id, task)
        # print(bound)
