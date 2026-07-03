"""sync_transactiontype_enum

Revision ID: 04ec85f71176
Revises: a4a965d56e6d
Create Date: 2026-07-03 19:45:00.000000

"""
from typing import Sequence, Union
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '04ec85f71176'
down_revision: Union[str, Sequence[str], None] = 'a4a965d56e6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

NEW_TYPE_VALUES = ('Transfer', 'Deposit', 'Withdrawal')


def upgrade() -> None:
    # 1. Drop the default on the type column
    op.execute("ALTER TABLE transactions ALTER COLUMN type DROP DEFAULT")

    # 2. Cast to VARCHAR
    op.execute("ALTER TABLE transactions ALTER COLUMN type TYPE VARCHAR USING type::text")

    # 3. Drop old enum
    op.execute("DROP TYPE IF EXISTS transactiontype")

    # 4. Create new enum with title-case values
    values_sql = ", ".join(f"'{v}'" for v in NEW_TYPE_VALUES)
    op.execute(f"CREATE TYPE transactiontype AS ENUM ({values_sql})")

    # 5. Map old ALL_CAPS values to new title-case values
    op.execute("UPDATE transactions SET type = 'Transfer' WHERE type = 'TRANSFER'")
    op.execute("UPDATE transactions SET type = 'Deposit' WHERE type = 'DEPOSIT'")
    op.execute("UPDATE transactions SET type = 'Withdrawal' WHERE type = 'WITHDRAWAL'")
    # Fallback for any other unexpected values
    op.execute("""
        UPDATE transactions SET type = 'Transfer'
        WHERE type NOT IN ('Transfer', 'Deposit', 'Withdrawal')
    """)

    # 6. Cast column back to new enum
    op.execute("ALTER TABLE transactions ALTER COLUMN type TYPE transactiontype USING type::transactiontype")

    # 7. Restore default
    op.execute("ALTER TABLE transactions ALTER COLUMN type SET DEFAULT 'Transfer'")


def downgrade() -> None:
    OLD_TYPE_VALUES = ('TRANSFER', 'DEPOSIT', 'WITHDRAWAL')

    op.execute("ALTER TABLE transactions ALTER COLUMN type DROP DEFAULT")
    op.execute("ALTER TABLE transactions ALTER COLUMN type TYPE VARCHAR USING type::text")
    op.execute("DROP TYPE IF EXISTS transactiontype")
    values_sql = ", ".join(f"'{v}'" for v in OLD_TYPE_VALUES)
    op.execute(f"CREATE TYPE transactiontype AS ENUM ({values_sql})")
    op.execute("UPDATE transactions SET type = 'TRANSFER'")
    op.execute("ALTER TABLE transactions ALTER COLUMN type TYPE transactiontype USING type::transactiontype")
    op.execute("ALTER TABLE transactions ALTER COLUMN type SET DEFAULT 'TRANSFER'")
