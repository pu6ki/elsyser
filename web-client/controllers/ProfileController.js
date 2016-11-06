import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';

export function ProfileController() {
    let dataFromAPI;
    return new Promise((resolve, reject) => {
        let profileUrl = 'http://127.0.0.1:8000/api/profile/';

        resolve(requester.getJSON(profileUrl));
    }).then((data) => {
        dataFromAPI = data;
        return new Promise((resolve, reject) => {
            resolve(templates.get('profile'));
        });
    }).then((res) => {
        let hbTemplate = Handlebars.compile(res),
            template = hbTemplate(dataFromAPI);

        $('#content').html(template);
    }).catch((err) => {
        console.log(err);
    });
}
