import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';

export function loginController() {
    let loginUrl = 'http://127.0.0.1:8000/api-token-auth/';

    templates.get('login')
        .then((res) => {
            return new Promise((resolve, reject) => {
                let hbTemplate = Handlebars.compile(res),
                    template = hbTemplate();

                $('#content').html(template);

                $('#loginButton').on('click', () => {
                    resolve(requester.postJSON(loginUrl, getDataFromTemplate()));
                });
            }).then((result) => {
                if (result.token) {
                    localStorage.setItem('token', result.token);
                    toastr.success('Logged-in successfully!');
                    window.location.href = '#/home';
                }
            }).catch((error) => {
                toastr.error('Couldn\'t log-in with the provided credentials!');
            });
        });
}

function getDataFromTemplate() {
    let body = {
        email: '',
        password: ''
    };

    body.email = $('#email').val();
    body.password = $('#password').val();

    return body;
}