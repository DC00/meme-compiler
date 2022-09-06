from xml.dom.minidom import Identified
from psycopg2 import sql

class Queries:

    @classmethod
    def metadata_exists(cls):
        return sql.SQL(
            """
            SELECT EXISTS(
                SELECT 1 FROM {table}
                WHERE 1=1
                AND platform = %s
                AND identifier = %s
            )
            """
        ).format(table=sql.Identifier("metadata"))

    @classmethod
    def insert_metadata(cls):
        return sql.SQL(
            """
            INSERT INTO {table} ({fields}) VALUES %s
            ON CONFLICT ({fields})
                DO UPDATE SET updated_at = now()::timestamp(0)
            """
        ).format(
            table=sql.Identifier("metadata"),
            fields=sql.SQL(", ").join(map(sql.Identifier, ["response_id", "url", "platform", "identifier", "filename"])),
            index=sql.SQL(", ").join(map(sql.Identifier, ["platform", "identifier"])),
        )

    @classmethod
    def select_responses(cls):
        return sql.SQL(
            """
            SELECT *
            FROM {table}
            WHERE {field} IS NULL
            LIMIT 5
            """
        ).format(
            table=sql.Identifier("responses"),
            field=sql.Identifier("video_id")
        )

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
