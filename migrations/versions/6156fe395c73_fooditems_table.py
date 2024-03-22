"""fooditems table

Revision ID: 6156fe395c73
Revises: 992e8375953c
Create Date: 2024-03-22 02:29:53.646829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6156fe395c73'
down_revision = '992e8375953c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('food_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('calories', sa.Integer(), nullable=False),
    sa.Column('protein', sa.Float(), nullable=False),
    sa.Column('carbs', sa.Float(), nullable=False),
    sa.Column('fat', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('food_item')
    # ### end Alembic commands ###
