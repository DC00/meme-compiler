import psycopg2
import json

from contextlib import contextmanager
from psycopg2 import extras
from psycopg2 import sql

class DatabaseService:

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        with open("config.json", "r") as f:
            data = json.loads(f.read())
            self.dbname   = data["dbname"]
            self.user     = data["dbuser"]
            self.password = data["dbpassword"]
            self.host     = data["dbhost"]

        return self

    @contextmanager
    def connection(self):
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host
        )

        yield conn

        conn.commit()
        conn.close()

    def add_responses(self, responses=[]):
        responses = [ (r.url, r.start_at, r.end_at) for r in responses if r.is_valid() ]

        query = Queries.insert_responses()

        with self.connection() as conn:
            cursor = conn.cursor()
            # https://www.psycopg.org/docs/extras.html#fast-execution-helpers ???
            extras.execute_values(cursor, query.as_string(conn), responses)

    def add_videos(self, videos=[]):
        videos = [ (v.platform, v.identifier) for v in videos if v.is_valid() ]

        query = Queries.insert_videos()

        with self.connection() as conn:
            cursor = conn.cursor()
            # https://www.psycopg.org/docs/extras.html#fast-execution-helpers ???
            extras.execute_values(cursor, query.as_string(conn), videos)

class Queries:

    @classmethod
    def insert_responses(cls):
        return sql.SQL(
            """
            INSERT INTO {table} ({fields}) VALUES %s
            ON CONFLICT ({index})
                DO UPDATE SET updated_at = now()::timestamp(0)
            """
        ).format(
            table=sql.Identifier("responses"),
            fields=sql.SQL(", ").join(map(sql.Identifier, ["url", "start_at", "end_at"])),
            index=sql.Identifier("url")
        )

    @classmethod
    def insert_videos(cls):
        return sql.SQL(
            """
            INSERT INTO {table} ({fields}) VALUES %s
            ON CONFLICT ({fields})
                DO UPDATE SET updated_at = now()::timestamp(0)
            """
        ).format(
            table=sql.Identifier("videos"),
            fields=sql.SQL(", ").join(map(sql.Identifier, ["platform", "identifier"])),
        )

