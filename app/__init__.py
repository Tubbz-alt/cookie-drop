from flask import Flask, render_template, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def home():
    return redirect(url_for('posts.home'))


from app.posts.views import mod as postsModule
app.register_blueprint(postsModule)
