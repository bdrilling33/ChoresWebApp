"""empty message

Revision ID: 0018d54ca70e
Revises: a0303496a300
Create Date: 2021-06-09 23:07:56.442501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0018d54ca70e'
down_revision = 'a0303496a300'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chore_progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('value', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chore_progress', schema=None) as batch_op:
        batch_op.drop_column('value')

    # ### end Alembic commands ###