import { HeaderController } from './controllers/HeaderController.js';
import { HomeController } from './controllers/HomeController.js';
import { LoginController } from './controllers/LoginController.js';
import { RegisterController } from './controllers/RegisterController.js';
import { LogoutController } from './controllers/LogoutController.js';
import { ProfileController } from './controllers/ProfileController.js';
import { ExamsController } from './controllers/ExamsController.js';
import { NewsController } from './controllers/NewsController.js';

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
    .on('#/logout', () => { LogoutController() })
    .resolve();
