"""create metadata table

Revision ID: 54a845289b0a
Revises: 5922ea1c1362
Create Date: 2022-09-05 15:57:12.039971

"""
import sqlalchemy as sa

from sqlalchemy import func
from sqlalchemy import cast

from alembic import op


# revision identifiers, used by Alembic.
revision = '54a845289b0a'
down_revision = '5922ea1c1362'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "metadata",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("response_id", sa.Integer, nullable=False),
        sa.Column("video_id", sa.Integer, nullable=False),
        sa.Column("url", sa.VARCHAR(255), nullable=False),
        sa.Column("platform", sa.VARCHAR(255), nullable=False),
        sa.Column("identifier", sa.VARCHAR(255), nullable=False),
        sa.Column("filename", sa.VARCHAR(255)),
        sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=cast(func.current_timestamp(0), sa.DateTime(timezone=False))),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=False, server_default=cast(func.current_timestamp(0), sa.DateTime(timezone=False)), onupdate=cast(func.current_timestamp(0), sa.DateTime(timezone=False)))
    )

    op.create_foreign_key(
        constraint_name="fk_response",
        source_table="metadata",
        referent_table="responses",
        local_cols=["response_id"],
        remote_cols=["id"],
        ondelete="SET NULL"
    )

    op.create_foreign_key(
        constraint_name="fk_video",
        source_table="metadata",
        referent_table="videos",
        local_cols=["video_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )

    op.create_index(
        "index_metadata_on_platform_and_identifier",
        "metadata",
        ["platform", "identifier"],
        unique=True
    )

def downgrade() -> None:
    op.drop_table("metadata")
