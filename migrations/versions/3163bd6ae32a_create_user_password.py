"""create user password

Revision ID: 3163bd6ae32a
Revises: 11672e4b0677
Create Date: 2023-03-05 16:42:19.863904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3163bd6ae32a'
down_revision = '11672e4b0677'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_password', sa.LargeBinary(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('_password')

    # ### end Alembic commands ###
