from models import Brand, Category, Item

def all_brands():
    return Brand.query.order_by("name")

def all_categories():
    return Category.query.order_by("name")

def all_items():
    return Item.query.order_by("id")