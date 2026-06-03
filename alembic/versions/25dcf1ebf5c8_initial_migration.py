"""Initial migration

Revision ID: 25dcf1ebf5c8
Revises: 
Create Date: 2026-05-13 09:05:57.708947

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25dcf1ebf5c8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('room_number', sa.String(), nullable=True),
        sa.Column('rent_price', sa.Integer(), nullable=True),
        sa.Column('service_fee', sa.Integer(), nullable=True),
        sa.Column('deposit', sa.Integer(), nullable=True),
        sa.Column('contact_info', sa.String(), nullable=True),
        sa.Column('move_in_date', sa.String(), nullable=True),
        sa.Column('electricity_type', sa.String(), nullable=True),
        sa.Column('fixed_electricity_fee', sa.Integer(), nullable=True),
        sa.Column('is_occupied', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_rooms_id'), 'rooms', ['id'], unique=False)
    op.create_index(op.f('ix_rooms_room_number'), 'rooms', ['room_number'], unique=True)
    op.create_table(
        'settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(), nullable=True),
        sa.Column('value', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key'),
    )
    op.create_index(op.f('ix_settings_id'), 'settings', ['id'], unique=False)
    op.create_table(
        'electricity_readings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=True),
        sa.Column('month', sa.Integer(), nullable=True),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('old_reading', sa.Integer(), nullable=True),
        sa.Column('new_reading', sa.Integer(), nullable=True),
        sa.Column('unit_price', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_electricity_readings_id'), 'electricity_readings', ['id'], unique=False)
    op.create_table(
        'monthly_bills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=True),
        sa.Column('month', sa.Integer(), nullable=True),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('electricity_fee', sa.Integer(), nullable=True),
        sa.Column('rent_fee', sa.Integer(), nullable=True),
        sa.Column('service_fee', sa.Integer(), nullable=True),
        sa.Column('total', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('prepaid_months', sa.String(), nullable=True),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
        sa.Column('tenant_name', sa.String(), nullable=True),
        sa.Column('move_in_date', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_monthly_bills_id'), 'monthly_bills', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_monthly_bills_id'), table_name='monthly_bills')
    op.drop_table('monthly_bills')
    op.drop_index(op.f('ix_electricity_readings_id'), table_name='electricity_readings')
    op.drop_table('electricity_readings')
    op.drop_index(op.f('ix_settings_id'), table_name='settings')
    op.drop_table('settings')
    op.drop_index(op.f('ix_rooms_room_number'), table_name='rooms')
    op.drop_index(op.f('ix_rooms_id'), table_name='rooms')
    op.drop_table('rooms')
