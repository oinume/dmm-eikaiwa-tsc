"""create teacher table

Revision ID: b237d39155
Revises:
Create Date: 2015-10-25 22:20:33.556733

"""

# revision identifiers, used by Alembic.
revision = 'b237d39155'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        "teacher",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, server_default=""),
    )


def downgrade():
    op.drop_table("teacher")
