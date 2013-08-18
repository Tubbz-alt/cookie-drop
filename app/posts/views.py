import datetime

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify
from werkzeug import check_password_hash, generate_password_hash

from flask_wtf import Form
from wtforms import TextField

from app import db
from app.posts.models import Post

mod = Blueprint('posts', __name__, url_prefix='/posts/')


@mod.route('')
def home():
    yesterday = datetime.datetime.utcnow() - datetime.timedelta(1)
    posts = Post.query.filter(Post.created_time > yesterday).order_by('created_time DESC').all()
    return render_template("posts/index.html", posts=posts)


@mod.route('list/<lat>/<long>', methods=['GET'])
def list(lat, long):
    #yesterday = datetime.datetime.utcnow() - datetime.timedelta(1)
    posts = Post.nearby_posts(lat, long, 1)
    return jsonify(result=[{'long': str(p.long), 'lat': str(p.lat), 'secret': p.secret} for p in posts]), 200


@mod.route('new', methods=['POST'])
def new():
    post = Post(secret=request.args.get('secret'),
            long=request.args.get('long'),
            lat=request.args.get('lat'))
    db.session.add(post)
    return jsonify(post)
