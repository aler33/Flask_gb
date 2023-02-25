from flask import Blueprint, render_template
from blog.views.users import USERS
from werkzeug.exceptions import NotFound

articles_app = Blueprint("articles_app", __name__)


# ARTICLES = ["Flask", "Django", "JSON:API"]
ARTICLES = {
    1: {
        'name': 'First article',
        'text': 'Text first article',
        'author': 1
    },
    2: {
        'name': 'Second article',
        'text': 'Text second article',
        'author': 2,
    },
    3: {
        'name': 'Third article',
        'text': 'Text second article',
        'author': 3,
    },
    4: {
        'name': 'Fourth article',
        'text': 'Text second article',
        'author': 1,
    }
}


@articles_app.route("/", endpoint="list")
def articles_list():
    return render_template("articles/list.html", articles=ARTICLES, users=USERS)


@articles_app.route("/<int:article_id>/", endpoint="details")
def article_details(article_id: int):
    try:
        article_name = ARTICLES[article_id]
    except KeyError:
        raise NotFound(f"Article #{article_id} doesn't exist")
    return render_template('articles/details.html', article_id=article_id, article_name=article_name, users=USERS)
