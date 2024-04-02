from flask import Flask, url_for
from flask_admin import Admin, expose, AdminIndexView, BaseView
from flask_login import LoginManager, login_required, current_user
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


class DashBoardView(AdminIndexView):
    @login_required
    @expose('/')
    def admin_panel(self):
        from src.models import User
        all_users = User.query.all()
        image_file = url_for('static',
                             filename=f'profile_pics' + '/users/' + current_user.username + '/account_img/' +
                                      current_user.image_file)
        return self.render('admin/index_admin.html', all_users=all_users, image_file=image_file)


class AnyPageView(BaseView):
    @expose('/')
    def any_page(self):
        return self.render('main/index.html')


admin = Admin(name='Admin Board', template_mode='bootstrap3', index_view=DashBoardView(), endpoint='admin')


def create_app():
    application = Flask(__name__)
    admin.init_app(application)
    application.config.from_pyfile('settings.py')
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
