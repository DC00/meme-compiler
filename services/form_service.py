import functools
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from response import *

class FormService:

    SHEET_OFFSET = 2
    COMPLETED_NOTE = "processed"
    CELL_RANGE = "'Form Responses 1'"
    INPUT_OPTION = "USER_ENTERED"

    @classmethod
    def build(cls, sheet_id):
        return cls(sheet_id).setup().read()

    def __init__(self, sheet_id):
        self.sheet_id = sheet_id

    def setup(self):
        self.creds, _ = google.auth.default()
        self.service = build("sheets", "v4", credentials=self.creds)

        return self

    def read(self):
        try:
            result = self.service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range=self.CELL_RANGE).execute()

            rows = result.get("values", [])
            rows.pop(0)
            rows = list(filter(None, rows))

            self.responses = [ Response(**self.params_for(row)) for row in rows ]
        except HttpError as error:
            print(f"An error occurred: {error}")

            return error

        return self

    def params_for(self, row):
        return {
            "timestamp": row[0],
            "url": row[1],
            "start_at": row[2] if len(row) > 2 else "",
            "end_at": row[3] if len(row) > 3 else ""
        }

    @functools.lru_cache(maxsize=10000)
    def urls(self):
        return [ response.url for response in self.responses if response.is_valid() ]

    def row_of(self, url):
        values = self.urls()

        return values.index(url) + self.SHEET_OFFSET if url in values else -1

    def update(self, url):
        row = self.row_of(url)

        if row > 0:
            range_name = f"'Form Responses 1'!C{row}"
            values = [ [self.COMPLETED_NOTE] ]
            body = { "values": values }

            return self.service.spreadsheets().values().update(spreadsheetId=self.sheet_id, range=range_name, valueInputOption=self.INPUT_OPTION, body=body).execute()

        return row

if __name__ == "__main__":
    sheet_id = "1oizPnNYIEzSLL6CrjlAMZdySw90jfTJf_2X9SFHejTM"

    fs = FormService.build(sheet_id)

    print(fs.urls())

    # url = "https://www.youtube.com/watch?v=ImUp_Yha3Ls"
    # fs.update(url)

