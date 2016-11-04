import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';

function homeController () {
    templates.get('home')
             .then((template) => {
                 $('#content').html(template);
             });
}

export { homeController };
