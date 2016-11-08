import { HeaderController } from './controllers/HeaderController.js';
import { HomeController } from './controllers/HomeController.js';

import { LoginController } from './controllers/AuthControllers/LoginController.js';
import { RegisterController } from './controllers/AuthControllers/RegisterController.js';
import { LogoutController } from './controllers/AuthControllers/LogoutController.js';

import { ProfileController } from './controllers/ProfileController.js';
import { ExamsController } from './controllers/ExamsController.js';

import { NewsController } from './controllers/NewsControllers/NewsController.js';
import { AddNewsController } from './controllers/NewsControllers/AddNewsController.js';
import { DetailedNewsController } from './controllers/NewsControllers/DetailedNewsController.js';

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
    .on('#/exams', () => {
        ExamsController();
    })
    .on('#/news', () => {
        NewsController();
    })
    .on('#/news/:id', (params) => {
        DetailedNewsController(params.id);
    })
    .on('#/add-news', () => {
        AddNewsController();
    })
    .on('#/homework', () => {
        HomeworksController();
    })
    .on('#/logout', () => { LogoutController() })
    .resolve();
