from app import db


class Url(db.Model):
    id = db.Column(db.Integer)
    original_url = db.Column(db.String, unique=True, nullable=False,)
    short_code = db.Column(db.String, primary_key=True)
