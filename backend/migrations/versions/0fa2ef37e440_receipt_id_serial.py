"""receipt id serial

Revision ID: 0fa2ef37e440
Revises: f6f97ed9c053
Create Date: 2023-07-25 21:26:25.353435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fa2ef37e440'
down_revision = 'f6f97ed9c053'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE SEQUENCE receipt_id_seq;")

    with op.batch_alter_table('receipt', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               server_default=sa.sql.func.next_value(sa.Sequence('receipt_id_seq')))

    with op.batch_alter_table('receipt_item', schema=None) as batch_op:
        batch_op.alter_column('receipt',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)

    op.execute("ALTER SEQUENCE receipt_id_seq OWNED BY receipt.id;")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('receipt_item', schema=None) as batch_op:
        batch_op.alter_column('receipt',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)

    with op.batch_alter_table('receipt', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)

    # ### end Alembic commands ###
