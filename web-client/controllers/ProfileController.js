import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';

export function ProfileController() {
    return new Promise((resolve, reject) => {
        let profileUrl = 'http://127.0.0.1:8000/api/profile/',
            token = window.localStorage.getItem('token'),
            authorizationHeader = `Authorization: Token ${token}`;

        resolve(requester.get(profileUrl, authorizationHeader));
    }).then((data) => {
        return new Promise((resolve, reject) => {
            resolve({
                template: templates.get('profile'),
                data
            });
        });
    }).then((res) => {
        let hbTemplate = Handlebars.compile(res.template),
            template = hbTemplate(res.data);

        $('#content').html(template);
    });
}