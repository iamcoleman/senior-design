"""empty message

Revision ID: 7867aeba65dc
Revises: 
Create Date: 2021-01-25 18:39:17.840045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7867aeba65dc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('analysis_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('keywords', sa.Text(), nullable=False),
    sa.Column('opened_at', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Enum('CREATED', 'LOADING_DATA', 'ANALYZING', 'READY', 'FAILURE', name='statusenum'), nullable=False),
    sa.Column('text_twitter', sa.Boolean(), nullable=True),
    sa.Column('text_reddit', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.LargeBinary(length=128), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    op.drop_table('users')
    op.drop_table('analysis_request')
    # ### end Alembic commands ###
