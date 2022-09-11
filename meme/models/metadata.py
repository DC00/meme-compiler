import sqlalchemy as sa

from sqlalchemy import func
from sqlalchemy import cast

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Metadata(Base):

    __tablename__ = "metadata"

    id          = sa.Column("id", sa.Integer, primary_key=True)
    response_id = sa.Column("response_id", sa.Integer, nullable=False)
    video_id    = sa.Column("video_id", sa.Integer, nullable=False)
    url         = sa.Column("url", sa.VARCHAR(255), nullable=False)
    platform    = sa.Column("platform", sa.VARCHAR(255), nullable=False)
    identifier  = sa.Column("identifier", sa.VARCHAR(255), nullable=False)
    filename    = sa.Column("filename", sa.VARCHAR(255))
    created_at  = sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=cast(func.current_timestamp(0), sa.DateTime(timezone=False)))
    updated_at  = sa.Column("updated_at", sa.TIMESTAMP, nullable=False, server_default=cast(func.current_timestamp(0), sa.DateTime(timezone=False)), onupdate=cast(func.current_timestamp(0), sa.DateTime(timezone=False)))

    PLATFORMS = ["youtube", "tiktok"]

    def __repr__(self):
        return f"Metadata(id={self.id}, response_id={self.response_id}, video_id={self.video_id}, url={self.url}, platform={self.platform}, identifier={self.identifier}, filename={self.filename}, created_at={self.created_at}, updated_at={self.updated_at}"

    def is_valid(self):
        return self.__valid_platform() and self.__valid_identifier()

    def key(self):
        return f"{self.platform}-{self.identifier}"

    def __valid_platform(self):
        if self.platform in self.PLATFORMS:
            return True

        return False

    def __valid_identifier(self):
        return len(self.identifier) > 0
