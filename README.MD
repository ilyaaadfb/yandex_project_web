Использованы модули:

        flask
        flask-admin
        flask-slugify
        flask-wtf
        flask-login
        flask-sqlalchemy
        flask-bcrypt
        python-dotenv
        email-validator
        ...



В файле requirements.txt находятся зависимости проекта. 
Установка зависимостей:
    
    pip install -r requirements.txt



Создать файл .env в корне папки site и записать туда переменные окружения

- FLASK_ENV=development
- FLASK_APP=run.py
- SQLALCHEMY_DATABASE_URI=sqlite:///site.db
- SQLALCHEMY_TRACK_MODIFICATIONS=True
- EMAIL_USER=YOUR_MAIL
- EMAIL_PASS=YOUR_PASS



Для запуска проекта используется файл

    run.py

Или на windows запускаем run
Или на linux запускаем run

Но тогда нужно сначлала создать базу данных с таблицами!
