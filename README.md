[![GitHub issues](https://img.shields.io/github/issues/pu6ki/elsyser.svg)](https://github.com/pu6ki/elsyser/issues)
[![GitHub forks](https://img.shields.io/github/forks/pu6ki/elsyser.svg)](https://github.com/pu6ki/elsyser/network)
[![GitHub stars](https://img.shields.io/github/stars/pu6ki/elsyser.svg)](https://github.com/pu6ki/elsyser/stargazers)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/pu6ki/elsyser/master/LICENSE)
[![Requires.io](https://img.shields.io/requires/github/pu6ki/elsyser.svg)](https://raw.githubusercontent.com/pu6ki/elsyser/master/requirements.txt)

# elsyser

**elsyser** is a *single page application (SPA), consuming RESTful services from the Django web server.*
This is a students' platform for ELSYS, Sofia.

## Prerequisites

- [Python v3.5+](https://www.python.org/downloads/)
- [pip v9.0.1](https://pypi.python.org/pypi/pip)
- [Node.js v7.0.0+](https://nodejs.org/en/)
- [npm v3.10.8](https://docs.npmjs.com/getting-started/installing-node)

## Tech

**elsyser** uses a number of open-source projects to work properly:

* [Django](https://github.com/django/django) - A really nice high-level Python web framework
* [Django Rest Framework](https://github.com/tomchristie/django-rest-framework) - Framework for building REST APIs in Django
* [django-cors-headers](https://github.com/ottoyiu/django-cors-headers) - Django app for handling the server headers required for Cross-Origin Resource Sharing (CORS)
* [drf-nested-routers](https://github.com/alanjds/drf-nested-routers) - Django Rest Framework nested routers
* [Pillow](https://github.com/python-pillow/Pillow) - Python Imaging Library
* [Bootstrap](https://github.com/twbs/bootstrap) - Framework for developing responsive UI on the web
* [jQuery](https://github.com/jquery/jquery) - New Wave JavaScript
* [handlebars](https://github.com/wycats/handlebars.js/) - Semantic templates for JavaScript
* [toastr](https://github.com/CodeSeven/toastr) - JavaScript library for representative notifications
* [navigo](https://github.com/krasimir/navigo) - Minimalistic JavaScript router
* [live-server](https://github.com/tapio/live-server) - A small HTTP web server with live reload
* [Atom](https://github.com/atom/atom) - A hackable text editor for the 21st century
* [Visual Studio Code](https://github.com/Microsoft/vscode) - Another cool text editor

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

6. Intstall Node.js dependencies:

    ```
    $ cd web-client/
    $ npm install
    $ npm install -g live-server
    ```

7. Run the live server:

    ```
    $ live-server
    ```

## Tutorial

1. `$ python3 manage.py runserver` and `$ live-server` should run simultaneously.
2. Visit http://127.0.0.1:8080/
3. Click "Register" to create your school account.
4. Then log in with your credentials.
5. Everything about you and your class is one click away!
    - Upcoming exams
    - Latest news with live comments
    - Assigned homeworks with materials for them
    - Profile info
    - ...

## The admin site

1. `$ python3 manage.py runserver`
2. Visit http://127.0.0.1:8000/admin/
3. Log in with your superuser data.
4. Here you can add, update and remove your models.

## Authors

We are students in 10th grade in ELSYS. We study programming and we are very enthusiastic about this project.

[![wencakisa](https://img.shields.io/badge/wencakisa-python-blue.svg)](https://github.com/wencakisa)
[![matir8](https://img.shields.io/badge/matir8-javascript-yellow.svg)](https://github.com/matir8)

### Task list:

- [ ] Make profile editable
- [x] Edit your own news
- [x] Edit and delete your own comments

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
