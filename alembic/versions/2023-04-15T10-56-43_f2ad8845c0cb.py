"""empty message

Revision ID: f2ad8845c0cb
Revises: 
Create Date: 2023-04-15 10:56:43.479772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2ad8845c0cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currency',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('currency_from', sa.VARCHAR(length=32), nullable=False),
    sa.Column('currency_to', sa.VARCHAR(length=32), nullable=False),
    sa.Column('amount', sa.FLOAT(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('currency')
    # ### end Alembic commands ###
