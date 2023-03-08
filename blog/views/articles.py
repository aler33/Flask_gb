from flask import Blueprint, render_template, request, current_app, redirect, url_for
# from blog.views.users import USERS
from werkzeug.exceptions import NotFound
from blog.models import User
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from blog.models.database import db
from blog.models import Article, Author
from blog.forms.article import  CreateArticleForm

articles_app = Blueprint("articles_app", __name__)


# ARTICLES = ["Flask", "Django", "JSON:API"]
# ARTICLES = {
#     1: {
#         'name': 'First article',
#         'text': 'Text first article',
#         'author': 4
#     },
#     2: {
#         'name': 'Second article',
#         'text': 'Text second article',
#         'author': 2,
#     },
#     3: {
#         'name': 'Third article',
#         'text': 'Text second article',
#         'author': 3,
#     },
#     4: {
#         'name': 'Fourth article',
#         'text': 'Text second article',
#         'author': 4,
#     }
# }


@articles_app.route("/", endpoint="list")
def articles_list():
    articles = Article.query.all()
    return render_template("articles/list.html", articles=articles)


@articles_app.route("/<int:article_id>/", endpoint="details")
def article_details(article_id: int):
    article = Article.query.filter_by(id=article_id).one_or_none()
    if article is None:
        raise NotFound
    return render_template("articles/details.html", article=article)


@articles_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        article = Article(title=form.title.data.strip(), body=form.body.data)
        db.session.add(article)
        if current_user.author:
            # use existing author if present
            article.author = current_user.author
        else:
            # otherwise create author record
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            article.author = current_user.author

        try:
            db.session.commit()
        except ImportError:
            current_app.logger.exception("Could not create a new article.")
            error = "Could not create article"
        else:
            return redirect(url_for("articles_app.details", article_id=article.id))

    return render_template("articles/create.html", form=form, error=error)
