"""establishment candidate table

Revision ID: 610854a6e2a0
Revises: 2be4d1ae5493
Create Date: 2023-03-18 13:36:12.953900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '610854a6e2a0'
down_revision = '2be4d1ae5493'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('establishment_candidate',
    sa.Column('user', sa.BigInteger(), nullable=False),
    sa.Column('establishment', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['establishment'], ['establishment.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user', 'establishment')
    )
    op.create_table('payment',
    sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
    sa.Column('token', sa.String(length=15), nullable=False),
    sa.Column('date', sa.Date(), server_default=sa.text('now()'), nullable=False),
    sa.Column('amount', sa.BigInteger(), server_default='0', nullable=False),
    sa.ForeignKeyConstraint(['token'], ['login_token.token'], ),
    sa.PrimaryKeyConstraint('id', 'token')
    )
    with op.batch_alter_table('login_token', schema=None) as batch_op:
        batch_op.alter_column('token',
               existing_type=sa.VARCHAR(length=15),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('login_token', schema=None) as batch_op:
        batch_op.alter_column('token',
               existing_type=sa.VARCHAR(length=15),
               nullable=True)

    op.drop_table('payment')
    op.drop_table('establishment_candidate')
    # ### end Alembic commands ###
