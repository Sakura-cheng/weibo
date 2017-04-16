"""add Article-comments_number

Revision ID: fbbd7f885b36
Revises: 78ca62e11cd2
Create Date: 2017-04-16 18:31:36.212106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbbd7f885b36'
down_revision = '78ca62e11cd2'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('comments_number', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'comments_number')
    ### end Alembic commands ###
