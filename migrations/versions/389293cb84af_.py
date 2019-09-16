"""empty message

Revision ID: 389293cb84af
Revises: d008f5a0cede
Create Date: 2019-09-16 11:36:27.505990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '389293cb84af'
down_revision = 'd008f5a0cede'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_date_key', 'users', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_date_key', 'users', ['date'])
    # ### end Alembic commands ###