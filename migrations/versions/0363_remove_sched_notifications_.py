"""

Revision ID: 0363_remove_sched_notifications
Revises: 0362_validate_constraint
Create Date: 2021-10-01 17:49:50.640582

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0363_remove_sched_notifications'
down_revision = '0362_validate_constraint'


def upgrade():
    # drop index concurrently will drop the index without locking out concurrent
    # selects, inserts, updates, and deletes on the index's table namely on notifications
    # First we need to issue a commit to clear the transaction block.
    op.execute('COMMIT')
    op.execute('DROP INDEX CONCURRENTLY ix_scheduled_notifications_notification_id')
    op.drop_table('scheduled_notifications')


def downgrade():
    # I've intentionally removed adding the index back from the downgrade method
    op.create_table('scheduled_notifications',
                    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
                    sa.Column('notification_id', postgresql.UUID(), autoincrement=False, nullable=False),
                    sa.Column('scheduled_for', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
                    sa.Column('pending', sa.BOOLEAN(), autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(['notification_id'], ['notifications.id'],
                                            name='scheduled_notifications_notification_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='scheduled_notifications_pkey')
                    )
