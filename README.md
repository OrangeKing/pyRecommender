# pyRecommend

## Synopsis
Django web application with movie recommendation support, Heroku-deployment ready.

## Running the application
*Application runs under Python 3.5.\**
*Prerequisites are postgreSQL, Python3 and PhantomJS for testing 3.5.\**
*For behavioral testing details, see README in pyBehave directory\**

1. **Install prerequisites:**
```shell
pip install -r requirements.txt
```

2. **Clone/fetch project**
```shell
git clone https://github.com/OrangeKing/pyRecommender.git
```

3. **Install postgreSQL database engine and create appropriate database:**
```SQL
CREATE DATABASE django_maps;
CREATE USER django_admin WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE django_maps TO django_admin;
ALTER USER django_admin CREATEDB;
\q
```

4. **Run:**
```shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Features
A program that functions as a RE with **moviedb recommendation support**. <br>
It allows to perform following activities:
* REGISTER new user
* LOG as newly registered user
* Localize any related keywords with use of moviedb API
* Add and modify articles / text content
* Remove articles / text content
* Preview content added by other users
* LOGOUT
