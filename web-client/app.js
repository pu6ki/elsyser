import { HeaderController } from './controllers/HeaderController.js';
import { HomeController } from './controllers/HomeController.js';

import { LoginController } from './controllers/AuthControllers/LoginController.js';
import { RegisterController } from './controllers/AuthControllers/RegisterController.js';
import { LogoutController } from './controllers/AuthControllers/LogoutController.js';

import { ProfileController } from './controllers/ProfileController.js';
import { EditProfileController } from './controllers/EditProfileController.js';

import { ExamsController } from './controllers/ExamsController.js';

import { NewsController } from './controllers/NewsControllers/NewsController.js';
import { AddNewsController } from './controllers/NewsControllers/AddNewsController.js';
import { DetailedNewsController, loadComments } from './controllers/NewsControllers/DetailedNewsController.js';

import { HomeworksController } from './controllers/HomeworksControllers/HomeworksController.js';


var handlebars = Handlebars || handlebars;
var router = new Navigo(null, false);

window.onbeforeunload = HeaderController();

router
    .on('/', () => { router.navigate('#/home') })
    .on('#/', () => { router.navigate('#/home') })
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
    .on('#/homework', () => {
        HomeworksController();
    })
    .on('#/logout', () => { LogoutController() })
    .resolve();
