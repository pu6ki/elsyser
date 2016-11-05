import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';

export function HomeController() {
    templates.get('home')
        .then((template) => {
            $('#content').html(template);
            if (window.localStorage.getItem('token')) {
                showLoggedInUserHeader();
            }
        });
}

function showLoggedInUserHeader() {
    $('#log-in').addClass('hide');
    $('#register').addClass('hide');
    $('#profile').removeClass('hide');
    $('#log-out').removeClass('hide');
}
