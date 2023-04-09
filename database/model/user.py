from database.db import db


# admin model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    refresh_token = db.Column(db.String(100), nullable=True, default='')
    access_token = db.Column(db.String(100), nullable=True, default='')

    admin = db.Column(db.Boolean, nullable=False, default=False)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'admin': self.admin,
        }

    def __repr__(self):
        return '<User %r>' % self.username
