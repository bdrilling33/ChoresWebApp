"""empty message

Revision ID: 9fe3db6d8a43
Revises: 7404091f3331
Create Date: 2021-06-10 10:13:30.994401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fe3db6d8a43'
down_revision = '7404091f3331'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chore_assignments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.String(length=3), nullable=True))

    with op.batch_alter_table('chore_progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('occurrence', sa.String(length=10), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chore_progress', schema=None) as batch_op:
        batch_op.drop_column('occurrence')

    with op.batch_alter_table('chore_assignments', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###
