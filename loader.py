import pickle

import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from category import Category
from word import Word
import config

class DataLoader:
    def __init__(self):

        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        self.SPREADSHEET_ID = config.TOKEN

        self.categories = []

        self.__prepare_creds()
    
    def __prepare_creds(self):
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    def load_data_from_web(self):

        service = build('sheets', 'v4', credentials=self.creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        sheet_metadata = sheet.get(spreadsheetId=self.SPREADSHEET_ID).execute()

        sheets = sheet_metadata.get("sheets", "")
        print("Reading", len(sheets), "sheets")
        for s in sheets:
            cat_name = s.get("properties", {}).get("title")
            self.categories.append(Category(cat_name))

            # read this sheet
            result = sheet.values().get(spreadsheetId=self.SPREADSHEET_ID,
                                        range=cat_name+"!A:Z").execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
            else:
                for v in values:
                    clue = v[0]
                    for sol in v[1:]:
                        self.categories[-1].add_word(Word(clue, sol))

    def store_to_file(self, fname):
        with open(fname, 'wb') as wf:
            pickle.dump(self.categories, wf)

    def load_from_file(self, fname):
        if os.path.exists(fname):
            with open(fname, 'rb') as wf:
                self.categories = pickle.load(wf)
            print("Successfully loaded", len(self.categories), "categories")
        else:
            print("Error: file not found")

    def get_categories(self):
        return self.categories
    
    def get_category(self, catName : str) -> Category:
        for c in self.categories:
            if str(c) == catName:
                return c
        print("Error: Category not found.")
        return None