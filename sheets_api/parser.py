import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Parser:
    creds = None

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
            for i in range(len(result) - 1):
                titles.append(result['sheets'][i]['properties']['title'])
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
