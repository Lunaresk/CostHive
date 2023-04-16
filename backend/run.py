from src import create_app, db
from src.models import Bought, Establishment, Item, LoginToken, Receipt, User, UserSchema

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Bought': Bought, 'Item': Item,
        "LoginToken": LoginToken, "Establishment": Establishment, "Receipt": Receipt,
        'UserSchema': UserSchema}