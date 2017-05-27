[![Heroku](http://heroku-badge.herokuapp.com/?app=elsyser&style=flat&root=/static/default.png)](https://elsyser.herokuapp.com/api/register)
[![GitHub stars](https://img.shields.io/github/stars/pu6ki/elsyser.svg?style=flat-square)](https://github.com/pu6ki/elsyser/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/pu6ki/elsyser.svg?style=flat-square)](https://github.com/pu6ki/elsyser/network)
[![GitHub issues](https://img.shields.io/github/issues/pu6ki/elsyser.svg?style=flat-square)](https://github.com/pu6ki/elsyser/issues)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://raw.githubusercontent.com/pu6ki/elsyser/master/LICENSE)
[![Requires.io](https://img.shields.io/requires/github/pu6ki/elsyser.svg?style=flat-square)](https://raw.githubusercontent.com/pu6ki/elsyser/master/requirements.txt)

![Logo](https://raw.githubusercontent.com/pu6ki/elsyser/master/static/tues_building_with_logo.jpg)

# [elsyser](https://elsyser.herokuapp.com/api/register/)

**elsyser** is a *RESTful API*, written in *Django*. This is part of a school platform that makes communication and resource sharing between students themselves and between students and their teachers easier.

## Prerequisites

- [Python v3.5+](https://www.python.org/downloads/)
- [pip v9.0.1+](https://pypi.python.org/pypi/pip)

## Tech

**elsyser** uses a number of open-source projects to work properly:

* [Django](https://github.com/django/django) - A really nice high-level Python web framework
* [Django Rest Framework](https://github.com/tomchristie/django-rest-framework) - Framework for building REST APIs in Django
* [django-cors-headers](https://github.com/ottoyiu/django-cors-headers) - Django app for handling the server headers required for Cross-Origin Resource Sharing (CORS)
* [drf-nested-routers](https://github.com/alanjds/drf-nested-routers) - Nested routing for DRF
* [Visual Studio Code](https://github.com/Microsoft/vscode) - A really nice text editor

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
2. Visit http://127.0.0.1:8000/api/register
3. Create your school account.
4. Then visit http://127.0.0.1:8000/api/login and log in with your credentials.
    - Here you will receive your authentication token, which you should pass as authentication header for further requests.
    ![Postman example](https://raw.githubusercontent.com/pu6ki/elsyser/master/static/authorization-example.png)
5. Enjoy! :D

## API URLs

### Students app:

- *POST* /api/register/ - Create new account.
- *POST* /api/login/ - Log in.
- /api/profile/:user_id/
    - *GET* - Personal info about the user.
    - *UPDATE* - Update profile info.
- *GET* /api/subjects/ - List of all subjects in the database.
- *GET* /api/classes/ - List of all classes in the database.
- *GET* /api/classes/:class_number/ - List of classes with that class number.
- *GET* /api/grades/:subject_id/ - Get list of grades for a certain subject.
- /api/grades/:subject_id/:user_id/
    - *GET* - List of grades for a certain user.
    - *POST* - Add a new grade for this user. **(only for teachers)**
- *GET* /api/students/:class_letter/:class_number/ - List of all students in a certain class.

### Exams app:

- /api/exams/
    - *GET*: List upcoming exams.
        - *Student acc*: Filters exams only for your class.
        - *Teacher acc*: Filters exams posted by this teacher.
    - *POST*: Schedule an exam. **(only for teachers)**

- /api/exams/:id/
    - *GET*: Show certain exam details.
    - *UPDATE*: Edit exam details. **(only for teachers)**
    - *DELETE*: Destroy an exam. **(only for teachers)**

### News app:

- **Common urls**:

***
- /api/news/*/
    - *GET* - Get news list for a certain group.
    - *POST* - Create a new post.
- /api/news/*/:id/
    - *GET* - Details about a certain post.
    - *UPDATE* - Update news' details.
    - *DELETE* - Destroy a news.
- /api/news/*/:id/comments/
    - *GET* - List comments linked with this news.
    - *POST* - Post a new comment linked with this post.
- /api/news/*/:id/comments/:comment_id/
    - *GET* - Show a certain comment.
    - *UPDATE* - Update comment's content.
    - *DELETE* - Destroy a comment.
***

- /api/news/students/
    - **only accessible by students**
    - All urls correspond the common ones above.

- /api/news/teachers/
    - **only accessible by teachers**
    - *GET* - List news posted by the current teacher.
- /api/news/teachers/:class_number/
    - *GET* - Get a list of the news posted by the current teacher for this class.
    - *POST* - Add news for all the classes with this class number.
- /api/news/teachers/:class_number/:class_letter/
    - All urls correspond to the common ones above.

### Homeworks app:

- /api/homeworks/
    - *GET* - List current homeworks.
        - *Student acc*: Homeworks about you.
        - *Teacher acc*: Homeworks, posted by you.
    - *POST* - Add a new homework **(only for teachers)**

- /api/homeworks/:id/
    - *GET* - Detailed information about a homework.
    - *UPDATE* - Update homework's info. **(only for teachers)**
    - *DELETE* - Destroy a homework. **(only for teachers)**

- /api/homeworks/:id/submissions/
    - *GET* - Get list of submissions that are not checked yet.
        - *Student acc*: Filters your submissions for this homework.
        - *Teacher acc*: Get submissions from all students.
    - *POST* - Submit a submission for a certain homework. **(only for students)**

- /api/homeworks/:id/submissions/:submission_id/
    - *GET* - Detailed information about a submission.
        - *Student acc*: Only if the submission is posted by you.
    - *UPDATE* - Update submission's details. **(only for students)**

### Materials app:

- /api/materials/ - List of useful materials.
    - *Student acc*: Filters materials only linked with your class.
    - *Teacher acc*: Filters materials only linked with your subject.

- /api/materials/:subject_id/ - Materials linked with a certain subject.
    - *GET* - List of these materials.
    - *POST* - Add a new material for your subject. **(only for teachers)**
    - *UPDATE* - Update material's content. **(only for teachers)**
    - *DELETE* - Remove a material. **(only for teachers)**


## The admin site

1. `$ python3 manage.py runserver`
2. Visit http://127.0.0.1:8000/admin/
3. Log in with your superuser data.
4. Here you can add, update and remove your models.

## Author

[wencakisa](https://github.com/wencakisa) - I am a student in 10th grade in ELSYS.
I am developing this back end service, used by [the ELSYSER web client](https://github.com/pu6ki/elsyser-web-client),
which is developed by my schoolmate [matir8](https://github.com/matir8).
Logo is designed by [Vladimir Vladinov](https://github.com/thehughmungus).

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
