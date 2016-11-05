import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';

export function IndexController() {
    let header = 'unauthorized';
    if(window.localStorage.getItem('token')) {
        header = 'authorized';
    }

    templates.get(header)
        .then((res) => {
            let hbTemplate = Handlebars.compile(res),
                template = hbTemplate();

            $('#header').html(template);
        });
}