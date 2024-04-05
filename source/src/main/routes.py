from flask import Blueprint, render_template, request
from flask_login import login_required

from src.models import Post, User

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def home():
    return render_template('main/index.html', title='Главная страница')


@main.route('/publication', methods=['POST', 'GET'])
@login_required
def src():
    all_posts = Post.query.order_by(Post.title.desc()).all()
    all_users = User.query.all()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)

    return render_template('main/log_in.html', title='Сайт', posts=posts,
                           all_posts=all_posts, all_users=all_users)
