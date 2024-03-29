"""Add table for logintoken de-/activation dates

Revision ID: 015f4256bb4c
Revises: 9a8c73f0ab11
Create Date: 2023-11-19 20:52:03.377745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '015f4256bb4c'
down_revision = '9a8c73f0ab11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('login_token_dates',
    sa.Column('token', sa.String(length=15), nullable=False),
    sa.Column('activation_date', sa.Date(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deactivation_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['token'], ['login_token.token'], ),
    sa.PrimaryKeyConstraint('token', 'activation_date')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('login_token_dates')
    # ### end Alembic commands ###
