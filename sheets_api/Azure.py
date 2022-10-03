import requests
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

personal_access_token = None


def connect_to_azure():
    global personal_access_token
    personal_access_token = '544t3yeqmfshd7klnnmisoau3g5cewtncrhpvgmpnoef7atzwpvq'
    organization_url = 'https://dev.azure.com/nikitau'
    credentials = BasicAuthentication('', personal_access_token)
    Connection(base_url=organization_url, creds=credentials)


def create_issue(header, url='https://dev.azure.com/nikitau/destination/_apis/wit/workitems/$Issue?api-version=6.0'):
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


def create_task(tasks, url='https://dev.azure.com/nikitau/destination/_apis/wit/workitems/$Task?api-version=6.0'):
    data = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": tasks[0].task_name,
        },
    ]
    req = requests.post(url, json=data, headers={'Content-Type': 'application/json-patch+json'},
                         auth=('', personal_access_token)).json()
    task_id = req['id']
    print(task_id)
    return task_id


def bound_tasks_and_issue(issue_id, task_id):
    url ='https://dev.azure.com/nikitau/destination/_apis/wit/workitems/{0}?api-version=6.1-preview.3'.format(task_id)
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
    task_id = create_task(tasks)
    print(bound_tasks_and_issue(issue_id, task_id))
