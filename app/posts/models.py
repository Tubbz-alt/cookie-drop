from app import db
import datetime


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    secret = db.Column(db.String(512))
    long = db.Column(db.Numeric(precision=8, scale=6))
    lat = db.Column(db.Numeric(prevision=8, scale=6))
    created_time = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, secret, long, lat):
        self.secret = secret
        self.long = long
        self.lat = lat
