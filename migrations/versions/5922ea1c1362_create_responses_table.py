"""create responses table

Revision ID: 5922ea1c1362
Revises: c8bb73b72889
Create Date: 2022-09-04 23:41:46.498062

"""
from tkinter.tix import COLUMN
from alembic import op
import sqlalchemy as sa


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
        sa.Column("video_id", sa.Integer, nullable=False),
        sa.Column("start_time", sa.VARCHAR(255)),
        sa.Column("end_time", sa.VARCHAR(255))
    )

    op.create_foreign_key(
        constraint_name="fk_video",
        source_table="responses",
        referent_table="videos",
        local_cols=["video_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )

def downgrade() -> None:
    op.drop_table("responses")
