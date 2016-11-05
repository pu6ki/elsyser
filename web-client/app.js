import { IndexController } from './controllers/IndexController.js';
import { HomeController } from './controllers/HomeController.js';
import { LoginController } from './controllers/LoginController.js';
import { RegisterController } from './controllers/RegisterController.js';
import { LogoutController } from './controllers/LogoutController.js';
import { ProfileController } from './controllers/ProfileController.js';
import { ExamsController } from './controllers/ExamsController.js';
import { NewsController } from './controllers/NewsController.js';

var handlebars = Handlebars || handlebars;
var router = new Navigo(null, false);

router
    .on('/', () => { router.navigate('#/home') })
    .on('#/', () => { router.navigate('#/home') })
    .on('#/home', () => {
        IndexController();
        HomeController();
    })
    .on('#/login', () => {
        IndexController();
        LoginController();
    })
    .on('#/register', () => {
        IndexController();
        RegisterController();
    })
    .on('#/profile', () => {
        IndexController();
        ProfileController();
    })
    .on('#/exams', () => {
        IndexController();
        ExamsController();
    })
    .on('#/news', () => {
        IndexController();
        NewsController();
    })
    .on('#/logout', () => { LogoutController() })
    .resolve();
