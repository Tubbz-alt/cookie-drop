from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash

from app import db
from app.posts.models import Post

mod = Blueprint('posts', __name__, url_prefix='/posts')


@mod.route('')
def home():
    yesterday = datetime.datetime.utcnow() - datetime.timedelta(1)
    posts = Post.query.filter_by(Post.created_time > yesterday).order_by('created_time DESC').all()
    return render_template("posts/index.html", posts=posts)
