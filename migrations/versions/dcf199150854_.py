"""empty message

Revision ID: dcf199150854
Revises: 9fe3db6d8a43
Create Date: 2021-06-10 17:08:31.599478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcf199150854'
down_revision = '9fe3db6d8a43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chore_progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assigned_user', sa.Integer(), nullable=True))
        batch_op.drop_column('assigned_user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chore_progress', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assigned_user_id', sa.INTEGER(), nullable=True))
        batch_op.drop_column('assigned_user')

    # ### end Alembic commands ###
