from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_values(spreadsheet_id, range_name):
    creds, _ = google.auth.default()
    try:
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        print(f"{len(rows)} rows retrieved")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    get_values("1CM29gwKIzeXsAppeNwrc8lbYaVMmUclprLuLYuHog4k", "A1:C2")
