"""create news archive table

Revision ID: 31efdc32af26
Revises: 2abfa7ba6e6b
Create Date: 2019-10-10 17:14:33.070419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31efdc32af26'
down_revision = '2abfa7ba6e6b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('newsarchive',
                    sa.Column('id', sa.Integer, nullable=False, autoincrement=True),
                    sa.Column('description', sa.Unicode, nullable=False),
                    sa.Column('url', sa.Unicode, nullable=False),
                    sa.Column('date_published', sa.DateTime(), nullable=False),
                    sa.Column('date_recorded', sa.DateTime(),
                                    server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('newsarchive')
    