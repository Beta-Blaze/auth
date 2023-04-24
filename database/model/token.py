from database.db import db


# Token black list model
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class TokenList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(16), nullable=False)
