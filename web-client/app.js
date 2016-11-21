import { HeaderController } from './controllers/HeaderController.js';
import { HomeController } from './controllers/HomeController.js';
import { AboutController } from './controllers/AboutController.js';

import { LoginController } from './controllers/AuthControllers/LoginController.js';
import { RegisterController } from './controllers/AuthControllers/RegisterController.js';

import { ProfileController } from './controllers/ProfileController.js';
import { EditProfileController } from './controllers/EditProfileController.js';

import { ExamsController } from './controllers/ExamsController.js';
import { DetailedExamsController } from './controllers/DetailedExamsController.js';

import { NewsController } from './controllers/NewsControllers/NewsController.js';
import { AddNewsController } from './controllers/NewsControllers/AddNewsController.js';
import { DetailedNewsController, loadComments } from './controllers/NewsControllers/DetailedNewsController.js';

import { DetailedHomeworkController } from './controllers/HomeworksControllers/DetailedHomeworkController.js';
import { HomeworksController } from './controllers/HomeworksControllers/HomeworksController.js';


var handlebars = Handlebars || handlebars;
HandlebarsIntl.registerWith(Handlebars);

var router = new Navigo(null, false);

window.onbeforeunload = HeaderController();

router
    .on('/', () => { router.navigate('#/home') })
    .on('#/', () => { router.navigate('#/home') })
    .on('#/about', () => {
        AboutController();
    })
    .on('#/home', () => {
        HeaderController();
        HomeController();
    })
    .on('#/login', () => {
        LoginController();
    })
    .on('#/register', () => {
        RegisterController();
    })
    .on('#/profile', () => {
        ProfileController();
    })
    .on('#/profile/edit', () => {
        EditProfileController();
    })
    .on('#/exams', () => {
        ExamsController();
    })
    .on('#/exams/:id', (params) => {
        DetailedExamsController(params.id);
    })
    .on('#/news', () => {
        NewsController();
    })
    .on('#/news/:id', (params) => {
        DetailedNewsController(params.id);
        let refreshId = setInterval(() => {
            loadComments(params.id);
            if (window.location.href !== `http://127.0.0.1:8080/#/news/${params.id}`) {
                clearInterval(refreshId);
            }
        }, 1000);
    })
    .on('#/add-news', () => {
        AddNewsController();
    })
    .on('#/news/:id/delete', (params) => {
        DeleteNewsController(params.id);
    })
    .on('#/homework', () => {
        HomeworksController();
    })
    .on('#/homework/:id', (params) => {
        DetailedHomeworkController(params.id);
    })
    .resolve();