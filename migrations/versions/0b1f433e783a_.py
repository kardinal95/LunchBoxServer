"""empty message

Revision ID: 0b1f433e783a
Revises: f8654a775079
Create Date: 2019-07-29 17:46:39.379974

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '0b1f433e783a'
down_revision = 'f8654a775079'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_statuses',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=80), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('orders',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('client_id', sa.Integer(), nullable=False),
                    sa.Column('status_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('timeslot_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['client_id'], ['roles.id'], onupdate='CASCADE', ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['status_id'], ['order_statuses.id'], onupdate='CASCADE',
                                            ondelete='SET NULL'),
                    sa.ForeignKeyConstraint(['timeslot_id'], ['timeslots.id'], onupdate='CASCADE', ondelete='SET NULL'),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    op.drop_table('order_statuses')
    # ### end Alembic commands ###
