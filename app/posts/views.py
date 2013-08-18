import datetime

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify
from werkzeug import check_password_hash, generate_password_hash

from app import db
from app.posts.models import Post

mod = Blueprint('posts', __name__, url_prefix='/posts/')


@mod.route('')
def home():
    yesterday = datetime.datetime.utcnow() - datetime.timedelta(1)
    posts = Post.query.filter(Post.created_time > yesterday).order_by('created_time DESC').all()
    return render_template("posts/index.html", posts=posts)


@mod.route('list')
def list():
    yesterday = datetime.datetime.utcnow() - datetime.timedelta(1)
    posts = Post.query.filter(Post.created_time > yesterday).order_by('created_time DESC').all()
    return jsonify(result=posts)


@mod.route('new', methods=['POST'])
def new():
    post = Post(secret=request.args.get('secret'),
            long=request.args.get('long'),
            lat=request.args.get('lat'))
    db.session.add(post)
    return jsonify(post)

