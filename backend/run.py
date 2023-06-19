from src import create_app, db
from src.models import *

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Bought': Bought, "Brand": Brand, 'Item': Item,
            "LoginToken": LoginToken, "Establishment": Establishment, "Receipt": Receipt,
            "brandschema": BrandSchema(), "itemschema": ItemSchema(), "testitem": Item.query.get(4311501628485),
            "testuser": User.query.get(1)}
