"""empty message

Revision ID: 46f70698292b
Revises: 94d9050d1103
Create Date: 2023-11-29 14:03:48.064944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46f70698292b'
down_revision = '94d9050d1103'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('ix_user_location')
        batch_op.create_index(batch_op.f('ix_user_location'), ['location'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_location'))
        batch_op.create_index('ix_user_location', ['location'], unique=False)

    # ### end Alembic commands ###
