from src import ma
from ..user import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    id = ma.auto_field()
    email = ma.auto_field()
    password_hash = ma.auto_field()
