"""create videos table

Revision ID: c8bb73b72889
Revises:
Create Date: 2022-09-04 23:11:17.824575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8bb73b72889'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "videos",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("platform", sa.VARCHAR(255), nullable=False),
        sa.Column("identifier", sa.VARCHAR(255), nullable=False),
        sa.Column("storage_link", sa.VARCHAR(255)),
        sa.Column("format", sa.VARCHAR(255)),
    )

    op.create_index(
        "index_videos_on_platform_and_identifier",
        "videos",
        ["platform", "identifier"],
        unique=True
    )


def downgrade() -> None:
    op.drop_table("videos")
