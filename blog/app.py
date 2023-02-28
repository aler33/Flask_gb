from flask import Flask, request, g, render_template
from time import time
from blog.views.users import users_app
from blog.views.articles import articles_app
from blog.views.auth import login_manager, auth_app
from blog.models.database import db


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/blog.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/alexey/gb_lesson/Flask_g/Flask_gb/blog/blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "abcdefg123456"
db.init_app(app)

@app.before_request
def process_before_request():
    """
    Sets start_time to `g` object
    """
    g.start_time = time()


app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix="/articles")
app.register_blueprint(auth_app, url_prefix="/auth")

login_manager.init_app(app)


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


@app.cli.command("init-db")
def init_db():
    """
    Run in terminal:
    flask init-db
    """
    db.create_all()


@app.cli.command("create-users")
def create_users():
    """
    Run in terminal:
    flask create-users
    """
    from blog.models import User
    admin = User(username='admin', is_staff=True, email='admin@localhost.ru')
    james = User(username="James", email='james@localhost.ru')
    brian = User(username="Brian", email='brian@localhost.ru')
    peter = User(username="Peter", email='peter@localhost.ru')

    db.session.add(admin)
    db.session.add(james)
    db.session.add(brian)
    db.session.add(peter)
    db.session.commit()

    print("done! created users:", admin, james)
