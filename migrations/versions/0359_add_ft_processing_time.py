"""

Revision ID: 164f16d5ddba
Revises: 02700689d4f8
Create Date: 2021-09-15 14:08:32.444965

"""
from alembic import op
import sqlalchemy as sa


revision = '164f16d5ddba'
down_revision = '02700689d4f8'


def upgrade():
    op.create_table('ft_processing_time',
                    sa.Column('bst_date', sa.Date(), nullable=False),
                    sa.Column('messages_total', sa.Integer(), nullable=False),
                    sa.Column('messages_within_10_secs', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('bst_date')
                    )
    op.create_index(op.f('ix_ft_processing_time_bst_date'), 'ft_processing_time', ['bst_date'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_ft_processing_time_bst_date'), table_name='ft_processing_time')
    op.drop_table('ft_processing_time')
