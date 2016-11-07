import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';
import { formHandler } from '../utils/formHandler.js';

export function AddNewsController() {
    templates.get('add-news')
        .then((res) => {
            let hbTemplate = Handlebars.compile(res),
                template = hbTemplate();

            $('#content').html(template);

            formHandler();

            $('#add-news').on('click', () => {
                addNews();
            });
        });
}

function getDataFromTemplate() {
    let body = {
        title: '',
        content: ''
    };

    body.title = $('#news-title').val();
    body.content = $('#news-content').val();

    return body;
}

function addNews() {
    let newsUrl = 'http://127.0.0.1:8000/api/news/';
    requester.postJSON(newsUrl, getDataFromTemplate())
        .then((result) => {
            if (result) {
                toastr.success('News added!');
                window.location.href = '#/news';
            }
        }).catch(() => {
            toastr.error('Couldn\'t log-in with the provided credentials!');
        });
}