import sqlalchemy as sa

from sqlalchemy import func
from sqlalchemy import cast

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Video(Base):

    __tablename__ = "videos"

    id           = sa.Column("id", sa.Integer, primary_key=True)
    platform     = sa.Column("platform", sa.VARCHAR(255), nullable=False)
    identifier   = sa.Column("identifier", sa.VARCHAR(255), nullable=False)
    storage_link = sa.Column("storage_link", sa.VARCHAR(255))
    format       = sa.Column("format", sa.VARCHAR(255))
    created_at   = sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=cast(func.current_timestamp(0), sa.DateTime(timezone=False)))
    updated_at   = sa.Column("updated_at", sa.TIMESTAMP, nullable=False, server_default=cast(func.current_timestamp(0), sa.DateTime(timezone=False)), onupdate=cast(func.current_timestamp(0), sa.DateTime(timezone=False)))

    PLATFORMS = ["youtube", "tiktok"]

    def __repr__(self):
        return f"Video(id={self.id}, platform={self.platform}, identifier={self.identifier}, storage_link={self.storage_link}, format={self.format})"

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
