"""empty message

Revision ID: 7a3e25a27afa
Revises: f2ad8845c0cb
Create Date: 2023-04-15 11:05:32.157196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a3e25a27afa'
down_revision = 'f2ad8845c0cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('currency', sa.Column('created_at', sa.TIMESTAMP(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('currency', 'created_at')
    # ### end Alembic commands ###
