import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';
import { formHandler } from '../utils/formHandler.js';


export function RegisterController() {
    templates.get('register')
        .then((res) => {
            return new Promise((resolve, reject) => {
                let hbTemplate = Handlebars.compile(res),
                    template = hbTemplate();

                $('#content').html(template);
                formHandler();

                $('#registerButton').on('click', () => {
                    register();
                });
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

function register() {
    let registerUrl = 'http://127.0.0.1:8000/api/register/';
    requester.postJSON(registerUrl, getDataFromTemplate())
        .then((result) => {
            if (result) {
                toastr.success('Registered successfully! Now you can log-in!');
                window.location.href = '#/login';
            }
        }).catch((error) => {
            toastr.error(`Couldn\'t register with the provided info! ${error.responseText}`);
        });
}
