import { requester } from '../../utils/requster.js';
import { templates } from '../../utils/templates.js';
import { formHandler } from '../../utils/formHandler.js';

export function LoginController() {
    templates.get('login')
        .then((res) => {
            return new Promise((resolve, reject) => {
                let hbTemplate = Handlebars.compile(res),
                    template = hbTemplate();

                $('#content').html(template);
                formHandler();

                $('#login-button').on('click', () => {
                    login();
                });
            });
        });
}

function getDataFromTemplate() {
    let body = {
        email_or_username: '',
        password: ''
    };

    body.email_or_username = $('#email-or-username').val();
    body.password = $('#password').val();

    return body;
}

function login() {
    let loginUrl = 'http://127.0.0.1:8000/api/login/';
    requester.postJSON(loginUrl, getDataFromTemplate())
        .then((result) => {
            if (result.token) {
                localStorage.setItem('token', result.token);
                toastr.success('Logged-in successfully!');
                window.location.href = '#/home';
            }
        }).catch(() => {
            toastr.error('Couldn\'t log-in with the provided credentials!');
        });
}

