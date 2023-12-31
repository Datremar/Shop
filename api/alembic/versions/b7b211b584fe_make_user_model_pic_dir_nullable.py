"""make user model pic_dir nullable

Revision ID: b7b211b584fe
Revises: 19e84f4de646
Create Date: 2023-11-09 12:20:24.557876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7b211b584fe'
down_revision: Union[str, None] = '19e84f4de646'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Users', 'profile_pic_dir',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Users', 'profile_pic_dir',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
