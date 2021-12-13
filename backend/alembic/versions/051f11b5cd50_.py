"""empty message

Revision ID: 051f11b5cd50
Revises:
Create Date: 2021-12-13 16:52:55.955071

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '051f11b5cd50'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task', sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=120), nullable=True),
                    sa.Column('points', sa.Integer(), nullable=True), sa.PrimaryKeyConstraint('id'))  # NOQA E501
    op.create_index(op.f('ix_task_name'), 'task', ['name'], unique=True)
    op.create_table('user', sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('wallet', sa.String(length=120), nullable=True),
                    sa.Column('total_points', sa.Integer(), nullable=True), sa.PrimaryKeyConstraint('id'))  # NOQA E501
    op.create_index(op.f('ix_user_wallet'), 'user', ['wallet'], unique=True)
    op.create_table(
        'completed',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_user', sa.Integer(), nullable=True),
        sa.Column(
            'id_task',
            sa.Integer(),  # NOQA E501
            nullable=True),
        sa.ForeignKeyConstraint(
            ['id_task'],
            ['task.id'],
        ),
        sa.ForeignKeyConstraint(
            ['id_user'],
            ['user.id'],
        ),
        sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_completed_id_task'), 'completed', ['id_task'], unique=False)
    op.create_index(op.f('ix_completed_id_user'), 'completed', ['id_user'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_completed_id_user'), table_name='completed')
    op.drop_index(op.f('ix_completed_id_task'), table_name='completed')
    op.drop_table('completed')
    op.drop_index(op.f('ix_user_wallet'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_task_name'), table_name='task')
    op.drop_table('task')
    # ### end Alembic commands ###
