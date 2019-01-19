"""empty message

Revision ID: 64cbfdf2d8d1
Revises: 84caedd23778
Create Date: 2019-01-19 19:10:16.607000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64cbfdf2d8d1'
down_revision = '84caedd23778'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hawker_centre', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('hawker_centre', sa.Column('longitude', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hawker_centre', 'longitude')
    op.drop_column('hawker_centre', 'latitude')
    # ### end Alembic commands ###