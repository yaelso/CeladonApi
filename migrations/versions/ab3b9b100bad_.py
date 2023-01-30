"""empty message

Revision ID: ab3b9b100bad
Revises: 10138b19fba6
Create Date: 2023-01-30 13:48:15.587420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab3b9b100bad'
down_revision = '10138b19fba6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('checklist', sa.Column('is_archived', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('checklist', 'is_archived')
    # ### end Alembic commands ###
