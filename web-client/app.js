import { HomeController } from './controllers/HomeController.js';
import { LoginController } from './controllers/LoginController.js';
import { RegisterController } from './controllers/RegisterController.js';
import { LogoutController } from './controllers/LogoutController.js';

var handlebars = Handlebars || handlebars;
var router = new Navigo(null, false);

router
    .on('/', () => { router.navigate('#/home') })
    .on('#/', () => { router.navigate('#/home') })
    .on('#/home', () => { HomeController() })
    .on('#/login', () => {
         if (LoginController()) {
             router.navigate('#/home');
         } 
        })
    .on('#/register', () => { RegisterController() })
    .on('#/logout', () => { LogoutController() })
    .resolve();