"""create views

Revision ID: 3d5fb9e86939
Revises: dbf88acb76bc
Create Date: 2022-02-20 01:58:37.444542

"""
from alembic import op
import sqlalchemy as sa

from app import db
from app.utils.view_utils import selectable_price_per_amount_view, selectable_bought_with_prices_view
from sqlalchemy_utils import create_view


# revision identifiers, used by Alembic.
revision = '3d5fb9e86939'
down_revision = 'dbf88acb76bc'
branch_labels = None
depends_on = None


def upgrade():
    metadata = sa.MetaData()
    create_view('price_per_amount',
        selectable_price_per_amount_view(),
        metadata
    )
    create_view('bought_with_prices',
        selectable_bought_with_prices_view(),
        metadata
    )
    metadata.create_all(db.engine)


def downgrade():
    with db.engine.connect() as con:
        con.execute("DROP VIEW bought_with_prices;")
        con.execute("DROP VIEW price_per_amount;")
