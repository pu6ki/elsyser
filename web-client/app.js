import { HeaderController } from './controllers/HeaderController.js';
import { HomeController } from './controllers/HomeController.js';

import { LoginController } from './controllers/AuthControllers/LoginController.js';
import { RegisterController } from './controllers/AuthControllers/RegisterController.js';
import { LogoutController } from './controllers/AuthControllers/LogoutController.js';

import { ProfileController } from './controllers/ProfileController.js';
import { EditProfileController } from './controllers/EditProfileController.js';

import { ExamsController } from './controllers/ExamsController.js';
import { DetailedExamsController } from './controllers/DetailedExamsController.js';

import { NewsController } from './controllers/NewsControllers/NewsController.js';
import { AddNewsController } from './controllers/NewsControllers/AddNewsController.js';
import { DetailedNewsController, loadComments } from './controllers/NewsControllers/DetailedNewsController.js';
import { DeleteNewsController } from './controllers/NewsControllers/DeleteNewsController.js';
import { EditNewsController } from './controllers/NewsControllers/EditNewsController.js';
import { DeleteCommentController } from './controllers/NewsControllers/DeleteCommentController.js';
import { EditCommentController } from './controllers/NewsControllers/EditCommentController.js';

import { DetailedHomeworkController } from './controllers/HomeworksControllers/DetailedHomeworkController.js';
import { HomeworksController } from './controllers/HomeworksControllers/HomeworksController.js';


var handlebars = Handlebars || handlebars;
HandlebarsIntl.registerWith(Handlebars);

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
    .on('#/news/:id/edit', (params) => {
        EditNewsController(params.id);
    })
    .on('#/news/:id/delete', (params) => {
        DeleteNewsController(params.id);
    })
    .on('#/news/:newsId/comments/:commentId/delete', (params) => {
        DeleteCommentController(params.newsId, params.commentId);
    })
    .on('#/news/:newsId/comments/:commentId/edit', (params) => {
        EditCommentController(params.newsId, params.commentId);
    }) 
    .on('#/homework', () => {
        HomeworksController();
    })
    .on('#/homework/:id', (params) => {
        DetailedHomeworkController(params.id);
    })
    .resolve();
