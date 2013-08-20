import datetime

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify
from werkzeug import check_password_hash, generate_password_hash

from flask_wtf import Form
from wtforms import TextField, HiddenField

from app import db
from app.posts.models import Post

mod = Blueprint('posts', __name__, url_prefix='/posts/')

# How far should we be able to see posts? (in miles)
POST_DISTANCE_THRESHOLD = 5


class NewPostForm(Form):
    long = HiddenField()
    lat = HiddenField()
    secret = TextField('Message')


@mod.route('')
def home():
    form = NewPostForm()
    return render_template("posts/index.html", form=form)


@mod.route('list/<lat>/<long>', methods=['GET'])
def list(lat, long):
    posts = Post.nearby_posts(lat, long, POST_DISTANCE_THRESHOLD)
    return jsonify(result=[{'long': str(p.long), 'lat': str(p.lat), 'secret': p.secret, 'created': str(p.created_time)} for p in posts]), 200


@mod.route('new', methods=['POST'])
def new():
    form = NewPostForm()
    post = Post()
    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()
        posts = Post.nearby_posts(post.lat, post.long, POST_DISTANCE_THRESHOLD)
        return jsonify(result=[{'long': str(p.long), 'lat': str(p.lat), 'secret': p.secret, 'created': str(p.created_time)} for p in posts]), 200
    return jsonify(result={'error': 'invalid form.'})
