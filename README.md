[![GitHub issues](https://img.shields.io/github/issues/pu6ki/elsyser.svg)](https://github.com/pu6ki/elsyser/issues)
[![GitHub forks](https://img.shields.io/github/forks/pu6ki/elsyser.svg)](https://github.com/pu6ki/elsyser/network)
[![GitHub stars](https://img.shields.io/github/stars/pu6ki/elsyser.svg)](https://github.com/pu6ki/elsyser/stargazers)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/pu6ki/elsyser/master/LICENSE)
[![Requires.io](https://img.shields.io/requires/github/pu6ki/elsyser.svg)](https://raw.githubusercontent.com/pu6ki/elsyser/master/requirements.txt)

# elsyser

**elsyser** is a *single page application (SPA), consuming RESTful services from the Django web server.*
This is a students' platform for ELSYS, Sofia. It's main purpose is to be helpful at our school.

## Prerequisites

- [Python 3.5+](https://www.python.org/downloads/)
- [pip 9.0.1](https://pypi.python.org/pypi/pip)
- [Node.js v7.0.0+](https://nodejs.org/en/)
- [npm 3.10.8](https://docs.npmjs.com/getting-started/installing-node)

## Tech

**elsyser** uses a number of open-source projects to work properly:

* [Django](https://github.com/django/django) - A really nice framework for Python web applications
* [Django Rest Framework](https://github.com/tomchristie/django-rest-framework) - Framework for building REST APIs in Django
* [Bootstrap](https://github.com/twbs/bootstrap) - Enhanced UI for modern websites
* [jQuery](https://github.com/jquery/jquery)
* [handlebars](https://github.com/wycats/handlebars.js/) - Semantic templates for JS
* [toastr](https://github.com/CodeSeven/toastr) - JS library for representative notifications
* [navigo](https://github.com/krasimir/navigo) - Minimalistic JS router
* [Atom](https://github.com/atom/atom) - A really nice text editor

## Getting started

How to copy this project to your local machine and run it:

1. Download a copy from GitHub:

    ```sh
    $ git clone https://github.com/pu6ki/elsyser.git
    $ cd elsyser/
    ```

2. Setup Django requirements:

    ```sh
    $ pip3 install -r requirements.txt
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    ```

3. Create a superuser:

    ```sh
    $ python3 manage.py createsuperuser
    ```

4. Run the tests:

    ```sh
    $ python3 manage.py test
    ```

5. Run the server locally:

    ```sh
    $ python3 manage.py runserver
    ```

6. Intstall NodeJS dependencies:

    ```sh
    $ cd web-client/
    $ npm install
    $ npm install live-server
    ```

7. Run the live server:

    ```sh
    $ live-server
    ```

## Tutorial

1. `python3 manage.py runserver` and `live-server` should run simultaneously.
2. Visit http://127.0.0.1:8080/
3. Click "Register" to create your school account.
4. Then log in with your credentials.
5. Everything about your class and you is one click away!
    - /exams: Upcoming exams
    - /news: Latest news
    - /homeworks: Assigned homeworks
    - /profile: Profile info
    - ...

## The admin site

1. `python3 manage.py runserver`
2. Visit http://127.0.0.1:8000/admin/
3. Log in with your superuser data.
4. Here you can add, update and remove your models.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Who are we?

We are two students in 10th grade in ELSYS. We study programming and we are very enthusiastic about this project.
* [**wencakisa**](https://github.com/wencakisa) - *Python*
* [**matir8**](https://github.com/matir8) - *HTML, CSS, JS*

### Task list:

- [ ] Make profile editable
- [ ] Edit your own news
- [ ] Edit and delete your own comments
