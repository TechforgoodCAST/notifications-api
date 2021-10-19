"""

Revision ID: 35986aeec764
Revises: 164f16d5ddba
Create Date: 2021-09-19 11:41:05.664282

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '35986aeec764'
down_revision = '164f16d5ddba'


def upgrade():
    op.create_table(
        'webauthn_credential',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),

        sa.Column('credential_data', sa.String(), nullable=False),
        sa.Column('registration_response', sa.String(), nullable=False),

        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),

        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('webauthn_credential')
