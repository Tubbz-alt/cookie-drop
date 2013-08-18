import datetime
from decimal import Decimal
from math import pi, sqrt, radians, cos
from geopy import distance, units

from sqlalchemy.ext.hybrid import hybrid_method

from app import db

EARTH_RADIUS_KM = 6371.009
KM_PER_DEG_LAT = 2 * pi * EARTH_RADIUS_KM / 360.0


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    secret = db.Column(db.String(512))
    long = db.Column(db.Numeric(precision=8, scale=6))
    lat = db.Column(db.Numeric(precision=8, scale=6))
    created_time = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    @hybrid_method
    def distance(self, lat, long):
        km_per_deg_long = KM_PER_DEG_LAT * cos(radians(lat))
        return sqrt((KM_PER_DEG_LAT * (lat - self.lat)) ** 2 + (km_per_deg_long * (long - self.long)))

    @classmethod
    def nearby_posts(cls, lat, long, dist):
        nearby_posts = []
        d = distance.distance(miles=dist)
        rough_distance = Decimal(str(units.degrees(arcminutes=d.nm) * 2))
        lat_lower = Decimal(lat) - rough_distance
        lat_upper = Decimal(lat) + rough_distance
        long_lower = Decimal(long) - rough_distance
        long_upper = Decimal(long) + rough_distance
        posts = db.session.query(Post).filter(Post.lat.between(lat_lower, lat_upper))
        posts = posts.filter(Post.long.between(long_lower, long_upper)).order_by('id desc')
        for post in posts:
            exact_distance = distance.distance((post.lat, post.long), (lat, long))
            if exact_distance.miles <= dist:
                nearby_posts.append(post)
        return nearby_posts
