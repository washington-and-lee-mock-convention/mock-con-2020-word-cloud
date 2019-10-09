"""create wordcloud table

Revision ID: 2abfa7ba6e6b
Revises: 
Create Date: 2019-10-08 22:29:54.323823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2abfa7ba6e6b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('wordcloud',
                    sa.Column('id', sa.Integer, nullable=False, autoincrement=True),
                    sa.Column('word', sa.Unicode, nullable=False),
                    sa.Column('date_published', sa.DateTime(), nullable=False),
                    sa.Column('date_recorded', sa.DateTime(),
                                    server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('payloads')