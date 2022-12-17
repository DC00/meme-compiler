import functools
import json

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from meme.models import Response

class FormService:

    COLUMNS = {
        'Timestamp': 'A',
        'URL': 'B',
        'Start Time': 'C',
        'End Time': 'D',
        'Platform': 'E',
        'Identifier': 'F',
        'Filename': 'G'
    }

    SHEET_OFFSET = 2
    SHEET = "'Form Responses 1'"
    INPUT_OPTION = "RAW"

    @classmethod
    def build(cls):
        return cls().setup()

    def __init__(self):
        pass

    def setup(self):
        with open("config.json", "r") as f:
            data = json.loads(f.read())
            self.sheet_id = data["sheet_id"]

        self.creds, _ = google.auth.default()
        self.service = build("sheets", "v4", credentials=self.creds)

        return self

    def read(self):
        try:
            result = self.service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range=self.SHEET).execute()

            rows = result.get("values", [])
            rows.pop(0)
            rows = list(filter(None, rows))

            responses = [ Response(self.params_for(row)) for row in rows ]
            self.responses = [ response for response in responses if response.is_valid() ]

        except HttpError as error:
            print(f"An error occurred: {error}")

            return error

        return self.responses

    def params_for(self, row):
        return {
            "timestamp": row[0],
            "url": row[1],
            "start_at": row[2] if len(row) > 2 else "",
            "end_at": row[3] if len(row) > 3 else ""
        }

    def ingest(self, metadata):
        metadata = [ m for m in metadata if m is not None ]

        for data in metadata:
            self.update(data)

    @functools.lru_cache(maxsize=10000)
    def urls(self):
        return [ response.url for response in self.responses ]

    def row_of(self, url):
        values = self.urls()

        return values.index(url) + self.SHEET_OFFSET if url in values else -1

    def update(self, data):
        row = self.row_of(data.url)

        if row > 0:
            # A1 Notation: https://developers.google.com/sheets/api/guides/concepts#a1_notation
            # 'Form Responses 1'!E{row}:H{row}
            range_name = f"{self.SHEET}!{self.COLUMNS['Platform']}{row}:{self.COLUMNS['Filename']}{row}"
            values = [[ data.platform, data.identifier, data.filename ]]
            body = { "values": values }

            return self.service.spreadsheets().values().update(spreadsheetId=self.sheet_id, range=range_name, valueInputOption=self.INPUT_OPTION, body=body).execute()

        return row
