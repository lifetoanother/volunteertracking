"""empty message

Revision ID: c4a0135c84f5
Revises: bcdfd59345cc
Create Date: 2019-04-12 22:13:17.392991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4a0135c84f5'
down_revision = 'bcdfd59345cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user') as batch_op:
        batch_op.drop_column('token')
        batch_op.drop_column('token_expiration')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('token_expiration', sa.DATETIME(), nullable=True))
    op.add_column('user', sa.Column('token', sa.VARCHAR(length=32), nullable=True))
    op.create_index('ix_user_token', 'user', ['token'], unique=1)
    # ### end Alembic commands ###
