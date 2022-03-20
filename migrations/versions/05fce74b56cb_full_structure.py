"""full structure

Revision ID: 05fce74b56cb
Revises: 
Create Date: 2022-02-20 16:31:34.589805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05fce74b56cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('establishment',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('owner', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['owner'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receipt',
    sa.Column('id', sa.Numeric(precision=22, scale=0), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('registered', sa.Boolean(), server_default='False', nullable=False),
    sa.Column('paid', sa.SmallInteger(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('brand', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['brand'], ['brand.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('login_token',
    sa.Column('user', sa.BigInteger(), nullable=False),
    sa.Column('establishment', sa.BigInteger(), nullable=False),
    sa.Column('token', sa.String(length=15), nullable=True),
    sa.ForeignKeyConstraint(['establishment'], ['establishment.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user', 'establishment'),
    sa.UniqueConstraint('token')
    )
    op.create_table('amount_change',
    sa.Column('item', sa.BigInteger(), nullable=False),
    sa.Column('date', sa.Date(), server_default='2021-12-01', nullable=False),
    sa.Column('amount', sa.SmallInteger(), server_default='1', nullable=False),
    sa.ForeignKeyConstraint(['item'], ['item.id'], ),
    sa.PrimaryKeyConstraint('item', 'date')
    )
    op.create_table('bought',
    sa.Column('token', sa.String(length=15), nullable=False),
    sa.Column('item', sa.BigInteger(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('amount', sa.SmallInteger(), nullable=False),
    sa.Column('registered', sa.Boolean(), server_default='False', nullable=False),
    sa.Column('paid', sa.SmallInteger(), server_default='0', nullable=False),
    sa.ForeignKeyConstraint(['item'], ['item.id'], ),
    sa.ForeignKeyConstraint(['token'], ['login_token.token'], ),
    sa.PrimaryKeyConstraint('token', 'item', 'date')
    )
    op.create_table('item_category',
    sa.Column('item', sa.BigInteger(), nullable=False),
    sa.Column('category', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category'], ['category.id'], ),
    sa.ForeignKeyConstraint(['item'], ['item.id'], ),
    sa.PrimaryKeyConstraint('item', 'category')
    )
    op.create_table('item_receipt',
    sa.Column('receipt', sa.Numeric(precision=22, scale=0), nullable=False),
    sa.Column('item', sa.BigInteger(), nullable=False),
    sa.Column('amount', sa.SmallInteger(), nullable=False),
    sa.ForeignKeyConstraint(['item'], ['item.id'], ),
    sa.ForeignKeyConstraint(['receipt'], ['receipt.id'], ),
    sa.PrimaryKeyConstraint('receipt', 'item')
    )
    op.create_table('price_change',
    sa.Column('item', sa.BigInteger(), nullable=False),
    sa.Column('date', sa.Date(), server_default='2021-12-01', nullable=False),
    sa.Column('price', sa.SmallInteger(), nullable=False),
    sa.ForeignKeyConstraint(['item'], ['item.id'], ),
    sa.PrimaryKeyConstraint('item', 'date')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('price_change')
    op.drop_table('item_receipt')
    op.drop_table('item_category')
    op.drop_table('bought')
    op.drop_table('amount_change')
    op.drop_table('login_token')
    op.drop_table('item')
    op.drop_table('user')
    op.drop_table('receipt')
    op.drop_table('establishment')
    op.drop_table('category')
    op.drop_table('brand')
    # ### end Alembic commands ###
