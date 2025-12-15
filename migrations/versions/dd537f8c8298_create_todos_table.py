"""create todos table

Revision ID: dd537f8c8298
Revises: a669b6022b8d
Create Date: 2025-12-15 17:21:12.092802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd537f8c8298'
down_revision: Union[str, Sequence[str], None] = 'a669b6022b8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
