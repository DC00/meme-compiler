import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SHEET_ID = "1oizPnNYIEzSLL6CrjlAMZdySw90jfTJf_2X9SFHejTM"
RANGE = "'Form Responses 1'!B:B" # A1 Notation


def get_urls(spreadsheet_id, range_name):
    creds, _ = google.auth.default()

    try:
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        urls = result.get('values', [])
        urls.pop(0)
        urls = [ url[0] for url in urls ]
        print(urls)
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

if __name__ == '__main__':
    get_urls(SHEET_ID, RANGE)

