"""initial schema

Revision ID: 0001
Revises: 
Create Date: 2026-06-02 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Create Enums
    user_role_enum = postgresql.ENUM('client', 'consultant', 'admin', name='user_role_enum')
    user_role_enum.create(op.get_bind())

    consultation_status_enum = postgresql.ENUM('pending', 'confirmed', 'completed', 'cancelled', name='consultation_status_enum')
    consultation_status_enum.create(op.get_bind())

    transaction_status_enum = postgresql.ENUM('pending', 'paid', 'refunded', name='transaction_status_enum')
    transaction_status_enum.create(op.get_bind())

    chat_role_enum = postgresql.ENUM('user', 'assistant', name='chat_role_enum')
    chat_role_enum.create(op.get_bind())

    # 2. Create users table
    op.create_table('users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('role', user_role_enum, nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=True)

    # 3. Create consultations table
    op.create_table('consultations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('client_id', sa.UUID(), nullable=False),
        sa.Column('consultant_id', sa.UUID(), nullable=False),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', consultation_status_enum, server_default='pending', nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['client_id'], ['users.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['consultant_id'], ['users.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_consultations_client_id', 'consultations', ['client_id'], unique=False)
    op.create_index('idx_consultations_consultant_id', 'consultations', ['consultant_id'], unique=False)
    op.create_index('idx_consultations_scheduled_at', 'consultations', ['scheduled_at'], unique=False)

    # 4. Create transactions table
    op.create_table('transactions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('consultation_id', sa.UUID(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=3), server_default='USD', nullable=False),
        sa.Column('status', transaction_status_enum, server_default='pending', nullable=False),
        sa.Column('paid_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['consultation_id'], ['consultations.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )

    # 5. Create reviews table
    op.create_table('reviews',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('consultation_id', sa.UUID(), nullable=False),
        sa.Column('rating', sa.SmallInteger(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
        sa.ForeignKeyConstraint(['consultation_id'], ['consultations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('consultation_id')
    )

    # 6. Create chat_messages table
    op.create_table('chat_messages',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('role', chat_role_enum, nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('intent', sa.String(length=80), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_chat_messages_user_id', 'chat_messages', ['user_id'], unique=False)

def downgrade() -> None:
    # 1. Drop tables in reverse order
    op.drop_table('chat_messages')
    op.drop_table('reviews')
    op.drop_table('transactions')
    op.drop_table('consultations')
    op.drop_table('users')

    # 2. Drop Enums
    chat_role_enum = postgresql.ENUM('user', 'assistant', name='chat_role_enum')
    chat_role_enum.drop(op.get_bind())

    transaction_status_enum = postgresql.ENUM('pending', 'paid', 'refunded', name='transaction_status_enum')
    transaction_status_enum.drop(op.get_bind())

    consultation_status_enum = postgresql.ENUM('pending', 'confirmed', 'completed', 'cancelled', name='consultation_status_enum')
    consultation_status_enum.drop(op.get_bind())

    user_role_enum = postgresql.ENUM('client', 'consultant', 'admin', name='user_role_enum')
    user_role_enum.drop(op.get_bind())
