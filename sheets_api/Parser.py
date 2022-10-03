import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from sheets_api.Encoder import TaskEncoder
from sheets_api.Task import Task
import json


class Parser:
    _creds = None
    _selected_sheet = None

    @staticmethod
    def set_connection():
        global creds
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    @staticmethod
    def get_sheets(spread_sheet_id):
        try:
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()
            result = sheet.get(spreadsheetId=spread_sheet_id).execute()
            titles = []
            for _, value in enumerate(result['sheets']):
                titles.append(value['properties']['title'])
            if not result:
                print('No data found.')
            return titles
        except HttpError as err:
            print(err)

    @staticmethod
    def get_sheet(spread_sheet_id, range_name):
        try:
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spread_sheet_id, range=range_name).execute()
            values = result.get('values', [])
            global selected_sheet
            selected_sheet = values
            if not result:
                print('No data found.')

            for row in values:
                print()
                print('-' * 100)
                for cell in row:
                    print("{:<25}|".format(cell), end=" ")
            print()
            print('-' * 100)
        except HttpError as err:
            print(err)

    @staticmethod
    def parse_tasks():
        tasks = []
        is_content = False
        has_sub = False
        sub_tasks = []
        print(selected_sheet)
        for i, row in enumerate(selected_sheet):
            if not is_content:
                if 'Задача' and 'Подзадача' in row:
                    is_content = True
                    continue
                if len(row) != 0:
                    for j in row:
                        if j != '' and j is not None:
                            tasks.append(j)
            if has_sub:
                if not row:
                    has_sub = False
                if len(row) >= 3:
                    sub_task = Task(row[1])
                    sub_task.time = row[2]
                    if len(row) > 3:
                        sub_task.description = row[4]
                    sub_tasks.append(sub_task)
                else:
                    index = len(tasks)
                    tasks[index - 1].sub_tasks = sub_tasks
                    sub_tasks = []
            if is_content and row != [] and row[0] != '':
                if len(row) >= 1:
                    has_sub = True
                    tasks.append(Task(row[0]))
                elif len(row) >= 3:
                    has_sub = False
                    sub_tasks = []
                    task = Task(row[0])
                    task.time = row[2]
                    tasks.append(task)
        return tasks

    @staticmethod
    def serialize_to_json(obj_list):
        return json.dumps(obj_list, cls=TaskEncoder, ensure_ascii=False)
