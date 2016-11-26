[![GitHub stars](https://img.shields.io/github/stars/pu6ki/elsyser.svg?style=flat-square)](https://github.com/pu6ki/elsyser/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/pu6ki/elsyser.svg?style=flat-square)](https://github.com/pu6ki/elsyser/network)
[![GitHub issues](https://img.shields.io/github/issues/pu6ki/elsyser.svg?style=flat-square)](https://github.com/pu6ki/elsyser/issues)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://raw.githubusercontent.com/pu6ki/elsyser/master/LICENSE)
[![Requires.io](https://img.shields.io/requires/github/pu6ki/elsyser.svg?style=flat-square)](https://raw.githubusercontent.com/pu6ki/elsyser/master/requirements.txt)

# [elsyser](https://elsyser.herokuapp.com/api/register/)

**elsyser** is a *RESTful API*, used for [the ELSYSER web client](https://github.com/pu6ki/elsyser-web-client) - a
students' platform for [ELSYS, Sofia](http://elsys-bg.org).

## Prerequisites

- [Python v3.5+](https://www.python.org/downloads/)
- [pip v9.0.1](https://pypi.python.org/pypi/pip)

## Tech

**elsyser** uses a number of open-source projects to work properly:

* [Django](https://github.com/django/django) - A really nice high-level Python web framework
* [Django Rest Framework](https://github.com/tomchristie/django-rest-framework) - Framework for building REST APIs in Django
* [django-cors-headers](https://github.com/ottoyiu/django-cors-headers) - Django app for handling the server headers required for Cross-Origin Resource Sharing (CORS)
* [drf-nested-routers](https://github.com/alanjds/drf-nested-routers) - Django Rest Framework nested routers
* [Django suit](https://github.com/darklow/django-suit) - Modern theme for Django admin panel
* [Pillow](https://github.com/python-pillow/Pillow) - Python Imaging Library
* [Atom](https://github.com/atom/atom) - A hackable text editor for the 21st century

## Getting started

How to copy this project to your local machine and run it:

1. Download a copy from GitHub:

    ```
    $ git clone https://github.com/pu6ki/elsyser.git
    $ cd elsyser/
    ```

2. Setup Django requirements:

    ```
    $ pip3 install -r requirements.txt
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    ```

3. Create a superuser:

    ```
    $ python3 manage.py createsuperuser
    ```

4. Run the tests:

    ```
    $ python3 manage.py test
    ```

5. Run the server locally:

    ```
    $ python3 manage.py runserver
    ```

## Tutorial

1. `$ python3 manage.py runserver`
2. Visit https://elsyser.herokuapp.com/api/register
3. Create your school account.
4. Then visit https://elsyser.herokuapp.com/api/login and log in with your credentials.
    - Here you will receive your authentication token, which you should pass as authentication header for further requests.
    - Postman example: ![Postman example](https://raw.githubusercontent.com/pu6ki/elsyser/master/static/authorization-example.png)
5. You can view everything about you and your class:
    - */api/exams* - Upcoming exams about your class.
    - */api/news* - News about your class, which you can post and edit too. Each news has it's own comments.
    - */api/homeworks*
    - */api/profile*
    - ...

## The admin site

1. `$ python3 manage.py runserver`
2. Visit https://elsyser.herokuapp.com/admin/
3. Log in with your superuser data.
4. Here you can add, update and remove your models.

## Author

[wencakisa](https://github.com/wencakisa) - I am a student in 10th grade in ELSYS.
I am developing this back end service, used by [the ELSYSER web client](https://github.com/pu6ki/elsyser-web-client),
which is developed by my schoolmate [matir8](https://github.com/matir8).

### Task list:

- [ ] Implement teachers accounts creation
- [ ] Implement teachers creation/updating/deleting of exams and homeworks
- [x] Write tests for news deletion
- [x] Write tests for student info updating
- [x] Write tests for exams detail info
- [x] Write tests for exams detail view
- [x] Write tests for homeworks detail view
- [ ] Fix profile image updating in profile.
- [ ] Write tests for profile image updating.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
