"""add source to WordCloud

Revision ID: 5481b5c414a3
Revises: 31efdc32af26
Create Date: 2019-10-27 22:56:00.394655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5481b5c414a3'
down_revision = '31efdc32af26'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('wordcloud',
        sa.Column('source', sa.Unicode, nullable=False),
    )


def downgrade():
    op.drop_column('wordcloud', 'source')