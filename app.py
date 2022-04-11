from os import getenv
from flask import Flask, render_template
from werkzeug.exceptions import HTTPException
from dotenv import find_dotenv, load_dotenv
from flask_login import LoginManager

# from scripts.auth import auth
# from scripts.models import db, User
from server.pages import pages

load_dotenv(find_dotenv())

app = Flask(__name__)
# To making the source HTML look cleaner
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
# Point SQLAlchemy to Heroku database, changes url to correct format
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace(
    "postgres://", "postgresql://"
)
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")

app.register_blueprint(pages)
# app.register_blueprint(auth)


# login_manager = LoginManager()
# # can actually login from any screen
# login_manager.login_view = "routes.index"
# login_manager.init_app(app)


# @login_manager.user_loader
# def load_user(user_id):
#     "loading user for flask-login"
#     # pylint: disable=no-member
#     return db.session.get(User, user_id)


@app.errorhandler(Exception)
def handle_error(error):
    "error handler"
    code = 500
    if isinstance(error, HTTPException):
        code = error.code
        if code == 404:
            return render_template("404.html"), 404
    return render_template("500.html"), code


app.run(debug=True)

# db.init_app(app)


# # pylint: disable=unused-argument
# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     "to help prevent pool overflow"
#     db.session.remove()
#     db.engine.dispose()


# @app.teardown_request
# def shutdown_request(exception=None):
#     "to help prevent pool overflow"
#     db.session.remove()


# with app.app_context():
#     db.create_all()
