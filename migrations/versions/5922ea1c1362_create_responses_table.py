"""create responses table

Revision ID: 5922ea1c1362
Revises: c8bb73b72889
Create Date: 2022-09-04 23:41:46.498062

"""
import sqlalchemy as sa

from sqlalchemy import func
from sqlalchemy import cast

from alembic import op


# revision identifiers, used by Alembic.
revision = '5922ea1c1362'
down_revision = 'c8bb73b72889'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "responses",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("url", sa.VARCHAR(255), nullable=False),
        sa.Column("video_id", sa.Integer),
        sa.Column("start_at", sa.VARCHAR(255)),
        sa.Column("end_at", sa.VARCHAR(255)),
        sa.Column("entered_at", sa.TIMESTAMP),
        sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=cast(func.current_timestamp(0), sa.DateTime(timezone=False))),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=False, server_default=cast(func.current_timestamp(0), sa.DateTime(timezone=False)), onupdate=cast(func.current_timestamp(0), sa.DateTime(timezone=False)))
    )

    op.create_foreign_key(
        constraint_name="fk_video",
        source_table="responses",
        referent_table="videos",
        local_cols=["video_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )

    op.create_index(
        "index_responses_on_url",
        "responses",
        ["url"],
        unique=True
    )

def downgrade() -> None:
    op.drop_table("responses")
