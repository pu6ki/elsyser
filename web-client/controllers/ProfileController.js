import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';

export function ProfileController() {
    let profileUrl = 'http://127.0.0.1:8000/api/profile/',
        getData = requester.getJSON(profileUrl),
        getTemplate = templates.get('profile');

    Promise.all([getData, getTemplate])
        .then((result) => {
            let data = result[0],
                hbTemplate = Handlebars.compile(result[1]),
                template = hbTemplate(data);

            $('#content').html(template);
        }).catch((err) => {
            console.log(err);
        });
}
