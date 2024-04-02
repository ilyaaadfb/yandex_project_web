from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Статья', validators=[DataRequired()])
    category = SelectField('Категории', choices=[('Алгебра', 'алгебра'), ('Русский язык', 'русский язык'),
                                                 ('Английский', 'английский'), ('Информатика', 'информатика'),
                                                 ('История', 'история'), ('Обществознание', 'обществознание'),
                                                 ('Геометрия', 'геометрия'), ('Литература', 'литература'),
                                                 ('Физика', 'физика'), ('Химия', 'химия')])
    tag_form = StringField('Тэг')
    picture = FileField('Изображение (png, jpg)', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Опубликовать')


class PostUpdateForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Статья', validators=[DataRequired()])
    category = SelectField('Категории', choices=[('Алгебра', 'алгебра'), ('Русский язык', 'русский язык'),
                                                 ('Английский', 'английский'), ('Информатика', 'информатика'),
                                                 ('История', 'история'), ('Обществознание', 'обществознание'),
                                                 ('Геометрия', 'геометрия'), ('Литература', 'литература'),
                                                 ('Физика', 'физика'), ('Химия', 'химия')])
    picture = FileField('Изображение (png, jpg)', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Опубликовать')
