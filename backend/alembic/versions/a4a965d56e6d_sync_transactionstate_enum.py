"""sync_transactionstate_enum

Revision ID: a4a965d56e6d
Revises: 0bc2aac180c2
Create Date: 2026-07-03 19:41:04.188607

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a4a965d56e6d'
down_revision: Union[str, Sequence[str], None] = '0bc2aac180c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

NEW_ENUM_VALUES = (
    'Initiated',
    'Validating',
    'Customer Context Ready',
    'Feature Engineering',
    'ML Analysis',
    'Rule Engine',
    'AI Analysis',
    'AI Policy',
    'Customer Verification',
    'Awaiting Customer Response',
    'Pending Decision',
    'Approved',
    'Step Up Authentication',
    'Executing',
    'Completed',
    'Blocked',
    'Cancelled',
    'Failed',
)


def upgrade() -> None:
    # 1. Drop the default on the column
    op.execute("ALTER TABLE transactions ALTER COLUMN status DROP DEFAULT")

    # 2. Cast column to plain text so we can drop the old enum type
    op.execute("ALTER TABLE transactions ALTER COLUMN status TYPE VARCHAR USING status::text")

    # 3. Drop the old enum type
    op.execute("DROP TYPE IF EXISTS transactionstate")

    # 4. Create the new enum type with all required values
    values_sql = ", ".join(f"'{v}'" for v in NEW_ENUM_VALUES)
    op.execute(f"CREATE TYPE transactionstate AS ENUM ({values_sql})")

    # 5. Reset any existing rows that have old invalid enum values
    op.execute("""
        UPDATE transactions SET status = 'Initiated'
        WHERE status NOT IN ({values})
    """.format(values=", ".join(f"'{v}'" for v in NEW_ENUM_VALUES)))

    # 6. Cast the column back to the new enum type
    op.execute("ALTER TABLE transactions ALTER COLUMN status TYPE transactionstate USING status::transactionstate")

    # 7. Restore default
    op.execute("ALTER TABLE transactions ALTER COLUMN status SET DEFAULT 'Initiated'")


def downgrade() -> None:
    OLD_ENUM_VALUES = (
        'INITIATED', 'VALIDATION', 'RISK_ANALYSIS',
        'AWAITING_CUSTOMER_DECISION', 'APPROVED', 'COMPLETED', 'REJECTED'
    )

    op.execute("ALTER TABLE transactions ALTER COLUMN status DROP DEFAULT")
    op.execute("ALTER TABLE transactions ALTER COLUMN status TYPE VARCHAR USING status::text")
    op.execute("DROP TYPE IF EXISTS transactionstate")
    values_sql = ", ".join(f"'{v}'" for v in OLD_ENUM_VALUES)
    op.execute(f"CREATE TYPE transactionstate AS ENUM ({values_sql})")
    op.execute("UPDATE transactions SET status = 'INITIATED'")
    op.execute("ALTER TABLE transactions ALTER COLUMN status TYPE transactionstate USING status::transactionstate")
    op.execute("ALTER TABLE transactions ALTER COLUMN status SET DEFAULT 'INITIATED'")
