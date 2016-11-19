import { requester } from '../../utils/requster.js';
import { templates } from '../../utils/templates.js';
import { formHandler } from '../../utils/formHandler.js';
import { validator } from '../../utils/validator.js';

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

    if (validator.title($('#news-title').val())) {
        body.title = $('#news-title').val();
    }
    else {
        toastr.error('Title shoud be between 3 and 100 characters long!');
        return;
    }

    if (validator.content($('#news-content').val())) {
        body.content = $('#news-content').val();
    }
    else {
        toastr.error('Content shoud be between 5 and 10000 characters long!');
        return;
    }

    return body;
}

function addNews() {
    let newsUrl = 'http://127.0.0.1:8000/api/news/';
    let data = getDataFromTemplate();
    if (data) {
        requester.postJSON(newsUrl, data)
            .then((result) => {
                if (result) {
                    toastr.success('News added!');
                    window.location.href = '#/news';
                }
            }).catch(() => {
                toastr.error('Couldn\'t add the news Please check for errors!');
            });
    }
}
