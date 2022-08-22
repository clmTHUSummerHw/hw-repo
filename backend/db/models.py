from db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(32))
    def __init__(self, username, password) -> None:
        super().__init__()
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return '<User %r>' % self.username

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', backref=db.backref('projects', lazy='dynamic'))

    def __init__(self, name, user) -> None:
        super().__init__()
        self.name = name
        self.user = user

    def __repr__(self) -> str:
        return '<Project %r>' % self.name