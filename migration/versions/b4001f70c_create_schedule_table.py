"""create schedule table

Revision ID: b4001f70c
Revises: 51cb9badf50
Create Date: 2015-11-02 20:21:23.543826

"""

# revision identifiers, used by Alembic.
revision = 'b4001f70c'
down_revision = 'b237d39155'
branch_labels = None
depends_on = None

from alembic import op
import enum
import sqlalchemy as sa
from sqlalchemy import Integer
from sqlalchemy.types import TypeDecorator


class EnumType(TypeDecorator):
    """Store IntEnum as Integer"""

    impl = Integer

    def __init__(self, *args, **kwargs):
        self.enum_class = kwargs.pop('enum_class')
        TypeDecorator.__init__(self, *args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not isinstance(value, self.enum_class):
                raise TypeError("Value should %s type" % self.enum_class)
            return value.value

    def process_result_value(self, value, dialect):
        if value is not None:
            if not isinstance(value, int):
                raise TypeError("value should have int type")
            return self.enum_class(value)

ScheduleStatus = enum.Enum("ScheduleStatus", "reservable reserved finished")


def upgrade():
    op.create_table(
        "schedule",
        sa.Column("teacher_id", sa.Integer, primary_key=True, autoincrement=False),
        sa.Column("datetime", sa.DateTime, primary_key=True, autoincrement=False),
        sa.Column("status", EnumType(enum_class=ScheduleStatus), nullable=False),
    )


def downgrade():
    op.drop_table("schedule")
