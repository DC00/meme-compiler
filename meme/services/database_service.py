# import psycopg2
# import json
# import meme

# from contextlib import contextmanager
# from psycopg2 import extras
# from psycopg2.extras import RealDictCursor

# class DatabaseService:

#     @classmethod
#     def build(cls):
#         return cls().setup()

#     def setup(self):
#         with open("config.json", "r") as f:
#             data = json.loads(f.read())
#             self.dbname   = data["dbname"]
#             self.user     = data["dbuser"]
#             self.password = data["dbpassword"]
#             self.host     = data["dbhost"]

#         return self

#     @contextmanager
#     def connection(self):
#         conn = psycopg2.connect(
#             dbname=self.dbname,
#             user=self.user,
#             password=self.password,
#             host=self.host
#         )

#         yield conn

#         conn.commit()
#         conn.close()

#     def add_responses(self, responses=[]):
#         responses = [ (r.url, r.start_at, r.end_at) for r in responses if r.is_valid() ]

#         query = meme.Queries.insert_responses()

#         with self.connection() as conn:
#             cursor = conn.cursor()
#             # https://www.psycopg.org/docs/extras.html#fast-execution-helpers ???
#             extras.execute_values(cursor, query.as_string(conn), responses)

#     def get_responses(self):
#         query = meme.Queries.select_responses()

#         with self.connection() as conn:
#             cursor = conn.cursor(cursor_factory=RealDictCursor)
#             cursor.execute(query)
#             results = cursor.fetchall()

#         return [ meme.Response(dict(result)) for result in results ]

#     def add_videos(self, videos=[]):
#         videos = [ (v.platform, v.identifier) for v in videos if v.is_valid() ]

#         query = meme.Queries.insert_videos()

#         with self.connection() as conn:
#             cursor = conn.cursor()
#             # https://www.psycopg.org/docs/extras.html#fast-execution-helpers ???
#             extras.execute_values(cursor, query.as_string(conn), videos)

#     def add_metadata(self, metadata=[]):
#         metadata = [ (m.response_id, m.url, m.platform, m.identifier, m.filename) for m in metadata if m.is_valid() ]

#         query = meme.Queries.insert_metadata()

#         with self.connection() as conn:
#             cursor = conn.cursor()
#             # https://www.psycopg.org/docs/extras.html#fast-execution-helpers ???
#             extras.execute_values(cursor, query.as_string(conn), metadata)

#     def metadata_exists(self, metadata):
#         query = meme.Queries.metadata_exists()

#         with self.connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, [metadata.platform, metadata.identifier])
#             result = cursor.fetchone()

#         return result[0]
