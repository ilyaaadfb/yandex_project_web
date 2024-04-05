from flask import Flask
from flask_admin import expose, BaseView
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Авторизуйтесь, чтобы попасть на эту страницу!'

mail = Mail()


class AnyPageView(BaseView):
    @expose('/')
    def any_page(self):
        return self.render('main/index.html')


def create_app():
    application = Flask(__name__)
    application.config.from_pyfile('config.py')
    db.init_app(application)
    bcrypt.init_app(application)
    login_manager.init_app(application)
    migrate.init_app(application, db, render_as_batch=True)
    mail.init_app(application)

    from src.models import User, Post, Tg

    from src.main.routes import main
    from src.user.routes import users
    from src.post.routes import posts
    from src.errors.handlers import errors

    application.register_blueprint(main)
    application.register_blueprint(users)
    application.register_blueprint(posts)
    application.register_blueprint(errors)

    return application
