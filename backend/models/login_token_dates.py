from src import db

class LoginTokenDates(db.Model):
    token = db.Column(db.ForeignKey('login_token.token'),
                      nullable = False, primary_key=True,
                      server_onupdate=db.FetchedValue())
    activation_date = db.Column(db.Date,
                                nullable=False, primary_key=True,
                                server_default=db.func.now())
    deactivation_date = db.Column(db.Date, nullable=True)

    def __repr__(self) -> str:
        return f"<LoginTokenDates {self.token, self.activation_date, self.deactivation_date}>"