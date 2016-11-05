import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';

export function IndexController() {
    let header = 'unauthorized-header';
    if(window.localStorage.getItem('token')) {
        header = 'authorized-header';
    }

    templates.get(header)
        .then((res) => {
            let hbTemplate = Handlebars.compile(res),
                template = hbTemplate();

            $('#header').html(template);
        });
}