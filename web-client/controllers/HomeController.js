import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';

export function HomeController() {
    templates.get('home')
        .then((template) => {
            $('#content').html(template);
        });
}
