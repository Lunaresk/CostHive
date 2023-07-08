from src import db

item_category = db.Table("item_category",
    db.Column("item", db.ForeignKey("item.id"), primary_key=True, server_onupdate=db.FetchedValue()),
    db.Column("category", db.ForeignKey("category.id"), primary_key=True, server_onupdate=db.FetchedValue())
)