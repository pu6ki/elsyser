import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';


export function registerController() {
    let registerUrl = 'http://127.0.0.1:8000/api/register/';

    templates.get('register')
        .then((res) => {
            return new Promise((resolve, reject) => {
                let hbTemplate = Handlebars.compile(res),
                    template = hbTemplate();

                $('#content').html(template);

                $('#registerButton').on('click', () => {
                    resolve(requester.postJSON(registerUrl, getDataFromTemplate()));
                });
            }).then((result) => {
                if (result) {
                    window.location.href = '#/home';
                }
                else {
                    console.log(result);
                }
            });

        });
}

function getDataFromTemplate() {
    let body = {
        user: {
            first_name: '',
            last_name: '',
            email: '',
            password: '',
        },
        clazz: {
            number: null,
            letter: ''
        }
    };

    body.user.first_name = $('#firstName').val();
    body.user.last_name = $('#lastName').val();
    body.user.email = $('#email').val();
    body.user.password = $('#password').val();
    body.clazz.number = +$('#studentClassNumber').val();
    body.clazz.letter = $('#studentClassLetter').val();

    return body;
}