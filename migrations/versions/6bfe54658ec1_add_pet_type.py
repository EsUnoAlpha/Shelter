"""add pet type

Revision ID: 6bfe54658ec1
Revises: 323883457e38
Create Date: 2023-11-24 22:52:59.102032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6bfe54658ec1'
down_revision: Union[str, None] = '323883457e38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pets', sa.Column('pet_type', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pets', 'pet_type')
    # ### end Alembic commands ###
