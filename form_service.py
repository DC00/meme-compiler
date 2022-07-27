import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class FormService:

    @classmethod
    def build(cls, sheet_id, range_name):
        return cls(sheet_id, range_name).setup()

    def __init__(self, sheet_id, range_name):
        self.sheet_id   = sheet_id
        self.range_name = range_name

    def setup(self):
        self.creds, _ = google.auth.default()
        self.service  = build('sheets', 'v4', credentials=self.creds)
        return self

    def urls(self):
        try:
            result = self.service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_name).execute()

            urls = result.get('values', [])
            urls.pop(0)
            urls = [ url[0] for url in urls ]

            return urls
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def update(self, range_name, value_input_option, new_values):
        pass


if __name__ == '__main__':
    sheet_id = "1oizPnNYIEzSLL6CrjlAMZdySw90jfTJf_2X9SFHejTM"
    range_name = "'Form Responses 1'!B:B" # A1 Notation

    fs = FormService.build(sheet_id, range_name)
    print(fs.urls())

