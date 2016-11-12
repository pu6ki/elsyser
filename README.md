# elsyser
**elsyser** is a *single page application (SPA), consuming RESTful services from the Django web server.*<br/>
This is a students' system for ELSYS, Sofia. Upcoming exams, homeworks, news about your class, everything is here!<br/>
It's main purpose is to be helpful at our school. As soon as possible we wish to integrate it in the educational process.

## Prerequisites
- python 3.5
- pip 9.0.1
- nodejs 7.0.0
- npm 3.10.8

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
Follow the instructions to create your superuser.
7. Run the tests:
```
$ python3 manage.py test
```
4. Run the server locally:
```
$ python3 manage.py runserver
```
5. Setup NodeJS requirements:
```
$ cd web-client/
$ npm install
$ npm install live-sever
```
6. Run the live server:
```
$ live-server
```
This will automatically open the page at http://127.0.0.1:8080/

## Tutorial
1. 'python3 manage.py runserver' & 'live-server' should run simultaneously.
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
1. 'python3 manage.py runserver'
2. Visit http://127.0.0.1:8000/admin/
3. Log in with your superuser data.
4. Here you can add, update and remove your models.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Who are we?
We are two students in 10th grade in ELSYS. We study programming and we are very enthusiastic about this project.
* **wencakisa** - *Back-end (Python)* - https://github.com/wencakisa
* **matir8** - *Front-end (HTML, CSS, JS)* - https://github.com/matir8
