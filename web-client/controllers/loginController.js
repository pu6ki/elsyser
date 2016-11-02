import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';

export function loginController() {
    let authUrl = 'http://127.0.0.1:8000/api-token-auth/';

    templates.get('login')
        .then((res) => {
            let hbTemplate = Handlebars.compile(res),
                template = hbTemplate(),
                body = {
                    username: '',
                    password: ''
                };

            $('#content').html(template);

            $('#submit').on('click', () => {
                console.log('clicked');
                body.username = $('#username').val();
                body.password = $('#password').val();
                return requester.postJSON(authUrl, body)
                    .then((result) => {
                        if (result.token) {
                            console.log(result.token);
                            localStorage.setItem('token', result.token);
                        }
                    });
            })
        })
}