import { homeController } from './controllers/homeController.js';
import { loginController } from './controllers/loginController.js';

var handlebars = Handlebars || handlebars;
var router = new Navigo(null, false);

router
    //.on('/', () => { router.navigate('#/home') })
    .on('#/', () => { router.navigate('#/home') })
    .on('#/home', () => { homeController() })
    .on('#/login', () => { loginController() })
    .resolve();