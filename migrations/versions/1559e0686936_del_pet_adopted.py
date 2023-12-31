"""del pet adopted

Revision ID: 1559e0686936
Revises: 2167eda840d9
Create Date: 2023-11-25 16:25:20.637934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1559e0686936'
down_revision: Union[str, None] = '2167eda840d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pets', 'is_adopted')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pets', sa.Column('is_adopted', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###
