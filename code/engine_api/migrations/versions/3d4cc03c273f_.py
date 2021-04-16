"""empty message

Revision ID: 3d4cc03c273f
Revises: c9280442d7be
Create Date: 2021-03-22 11:48:36.858630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d4cc03c273f'
down_revision = 'c9280442d7be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('analysis_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('analysis_request_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['analysis_request_id'], ['analysis_request.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('text_tumblr',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('analysis_request_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('is_analyzed', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['analysis_request_id'], ['analysis_request.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('text_reddit', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('text_reddit', sa.Column('is_analyzed', sa.Boolean(), nullable=False))
    op.add_column('text_reddit', sa.Column('text', sa.Text(), nullable=False))
    op.alter_column('text_reddit', 'analysis_request_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('text_reddit', 'analysis_request_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('text_reddit', 'text')
    op.drop_column('text_reddit', 'is_analyzed')
    op.drop_column('text_reddit', 'created_at')
    op.drop_table('text_tumblr')
    op.drop_table('analysis_results')
    # ### end Alembic commands ###