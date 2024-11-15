"""Auto-generated migration 20240906_211112

Revision ID: 34e051d806d5
Revises: 
Create Date: 2024-09-06 21:11:13.134588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34e051d806d5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer_devices',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('device_type', sa.String(), nullable=True),
    sa.Column('device_os', sa.String(), nullable=True),
    sa.Column('device_name', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('last_accessed', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_devices_id'), 'customer_devices', ['id'], unique=False)
    op.create_table('customer_users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('country_code', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_user', sa.Integer(), nullable=True),
    sa.Column('updated_user', sa.Integer(), nullable=True),
    sa.Column('deleted_user', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_users_email'), 'customer_users', ['email'], unique=True)
    op.create_index(op.f('ix_customer_users_id'), 'customer_users', ['id'], unique=False)
    op.create_index(op.f('ix_customer_users_phone_number'), 'customer_users', ['phone_number'], unique=True)
    op.create_index(op.f('ix_customer_users_username'), 'customer_users', ['username'], unique=True)
    op.create_table('customer_otps',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('otp_code', sa.String(), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('expires_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['customer_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_otps_id'), 'customer_otps', ['id'], unique=False)
    op.create_index(op.f('ix_customer_otps_otp_code'), 'customer_otps', ['otp_code'], unique=True)
    op.create_table('customer_sessions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=True),
    sa.Column('host', sa.String(), nullable=True),
    sa.Column('access_token', sa.String(), nullable=True),
    sa.Column('refresh_token', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('last_accessed', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('expires_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['customer_devices.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['customer_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_sessions_access_token'), 'customer_sessions', ['access_token'], unique=True)
    op.create_index(op.f('ix_customer_sessions_id'), 'customer_sessions', ['id'], unique=False)
    op.create_index(op.f('ix_customer_sessions_refresh_token'), 'customer_sessions', ['refresh_token'], unique=True)
    op.create_table('customer_user_infos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('bio', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('birthdate', sa.DateTime(), nullable=True),
    sa.Column('profile_picture', sa.String(), nullable=True),
    sa.Column('country_code', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('contact_email', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_user', sa.Integer(), nullable=True),
    sa.Column('updated_user', sa.Integer(), nullable=True),
    sa.Column('deleted_user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['customer_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_user_infos_contact_email'), 'customer_user_infos', ['contact_email'], unique=True)
    op.create_index(op.f('ix_customer_user_infos_id'), 'customer_user_infos', ['id'], unique=False)
    op.create_index(op.f('ix_customer_user_infos_phone_number'), 'customer_user_infos', ['phone_number'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_customer_user_infos_phone_number'), table_name='customer_user_infos')
    op.drop_index(op.f('ix_customer_user_infos_id'), table_name='customer_user_infos')
    op.drop_index(op.f('ix_customer_user_infos_contact_email'), table_name='customer_user_infos')
    op.drop_table('customer_user_infos')
    op.drop_index(op.f('ix_customer_sessions_refresh_token'), table_name='customer_sessions')
    op.drop_index(op.f('ix_customer_sessions_id'), table_name='customer_sessions')
    op.drop_index(op.f('ix_customer_sessions_access_token'), table_name='customer_sessions')
    op.drop_table('customer_sessions')
    op.drop_index(op.f('ix_customer_otps_otp_code'), table_name='customer_otps')
    op.drop_index(op.f('ix_customer_otps_id'), table_name='customer_otps')
    op.drop_table('customer_otps')
    op.drop_index(op.f('ix_customer_users_username'), table_name='customer_users')
    op.drop_index(op.f('ix_customer_users_phone_number'), table_name='customer_users')
    op.drop_index(op.f('ix_customer_users_id'), table_name='customer_users')
    op.drop_index(op.f('ix_customer_users_email'), table_name='customer_users')
    op.drop_table('customer_users')
    op.drop_index(op.f('ix_customer_devices_id'), table_name='customer_devices')
    op.drop_table('customer_devices')
    # ### end Alembic commands ###
