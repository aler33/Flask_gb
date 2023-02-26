from flask import Flask, request, g, render_template
from time import time
from blog.views.users import users_app
from blog.views.articles import articles_app
from blog.models.database import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.before_request
def process_before_request():
    """
    Sets start_time to `g` object
    """
    g.start_time = time()


app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix="/articles")


@app.route("/")
def index():
    return render_template("index.html")


@app.after_request
def process_after_request(response):
    """
    adds process time in headers
    """
    if hasattr(g, "start_time"):
        response.headers["process-time"] = time() - g.start_time

    return response
