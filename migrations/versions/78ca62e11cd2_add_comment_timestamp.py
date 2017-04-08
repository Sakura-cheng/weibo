"""add comment-timestamp

Revision ID: 78ca62e11cd2
Revises: 
Create Date: 2017-04-08 19:52:56.316364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78ca62e11cd2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_comments_timestamp'), 'comments', ['timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comments_timestamp'), table_name='comments')
    op.drop_column('comments', 'timestamp')
    ### end Alembic commands ###