import os
import PIL
import sqlalchemy
from flask import (Blueprint, render_template, redirect, url_for, flash, abort, request, current_app)
from flask_login import current_user, login_required
from slugify import slugify

from src import db
from src.models import Post, Tag
from src.post.forms import PostForm, PostUpdateForm

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    try:
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, category=form.category.data,
                        image_post=form.picture.data, author=current_user)
            db.session.add(post)
            post.slug = slugify(post.title)
            db.session.flush()

            name = form.tag_form.data.split('/')
            for i in name:
                tag_post = Tag(name=i)  # создаю тег
                tag_post.post_id = post.id
                db.session.add(tag_post)
            db.session.commit()
            flash('Пост был опубликован!', 'success')
            return redirect(url_for('main.src'))
        else:
            if request.method == 'POST':
                flash('Формат изображения должен быть "jpg", "png"', 'success')
    except PIL.UnidentifiedImageError:
        flash('Выберите изображение для статьи', 'danger')
    except sqlalchemy.exc.IntegrityError:
        flash('Такой заголовок уже существует', 'danger')
        db.session.rollback()

    image_file = url_for('static',
                         filename=f'profile_pics/' + 'users/' + current_user.username + '/post_images/'
                                  + current_user.image_file)
    return render_template('post/create_post.html', title='Новая статья',
                           form_new_post=form, legend='Новая статья', image_file=image_file)


@posts.route('/post/<string:slug>', methods=['GET', 'POST'])
@login_required
def post(slug):
    post = Post.query.filter_by(slug=slug).first()
    form_post = PostForm()
    if request.method == 'POST':
        def add_tag():
            name = form_post.tag_form.data
            if name:
                name = name.split('/')
                for i in name:
                    tag_post = Tag(name=i)
                    tag_post.post_id = post.id
                    db.session.add(tag_post)
                db.session.commit()
                flash('Тег к посту был добавлен', "success")
                return redirect(url_for('posts.post', slug=post.slug))

        add_tag()
    form_post.tag_form.data = ''
    image_file = url_for('static',
                         filename=f'profile_pics/' + 'users/' + post.author.username + '/post_images/' + post.image_post)
    return render_template('post/post.html', title=post.title, post=post, image_file=image_file,
                           form_add_tag=form_post)


@posts.route('/post/<string:slug>/update', methods=['GET', 'POST'])
@login_required
def update_post(slug):
    post = Post.query.filter_by(slug=slug).first()

    if post.author != current_user:
        flash('Нет доступа к обновлению статьи!', 'danger')
        return redirect(url_for('posts.post', slug=post.slug))
    form = PostUpdateForm()
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data

        db.session.commit()

        flash('Данный пост был обновлён', 'success')

        return redirect(url_for('posts.post', slug=slug))
    else:
        if request.method == 'POST':
            flash('Формат изображения должен быть "jpg", "png"', 'success')
    image_file = url_for('static',
                         filename=f'profile_pics/users/{current_user.username}/post_images/{post.image_post}')

    return render_template('post/update_post.html', title='Обновление ' + post.title,
                           form_post_update=form, legend='Обновить статью', image_file=image_file, post=post)


@posts.route('/posts/<string:category_str>/', methods=['GET', 'POST'])
@login_required
def category(category_str):
    current_category = Post.query.filter_by(category=category_str).first()
    posts_category = Post.query.filter_by(category=category_str).all()
    return render_template('post/all_posts_category.html', post_category=posts_category,
                           current_category=current_category, title='Рубрика ' + category_str)


@posts.route('/tags/<string:tag_str>', methods=['GET', 'POST'])
@login_required
def tag(tag_str):
    current_tag = Tag.query.filter_by(name=tag_str).first_or_404()
    name_tags = Tag.query.filter(Tag.name == current_tag.name).all()
    return render_template('post/all_post_tag.html', name_tags=name_tags,
                           current_tag=current_tag, title='Статьи тега ' + current_tag.name)


@posts.route('/post/<string:slug>/delete', methods=['POST', 'GET'])
@login_required
def delete_post(slug):
    post = Post.query.filter_by(slug=slug).first()
    if post.author != current_user:
        abort(403)
    try:
        os.unlink(
            os.path.join(current_app.root_path,
                         f'static/profile_pics/users/{current_user.username}/post_images/{post.image_post}'))
        db.session.delete(post)
    except:
        db.session.delete(post)

    db.session.commit()
    flash('Данный пост был удален', 'success')
    return redirect(url_for('users.account'))
