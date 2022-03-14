"""empty message

Revision ID: 70e9d35806b0
Revises: dcf199150854
Create Date: 2022-03-14 11:29:28.456086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70e9d35806b0'
down_revision = 'dcf199150854'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('approval_code', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('approval_code')

    # ### end Alembic commands ###