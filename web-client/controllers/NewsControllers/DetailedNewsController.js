import { requester } from '../../utils/requster.js';
import { templates } from '../../utils/templates.js';
import { validator } from '../../utils/validator.js';
import { formHandler } from '../../utils/formHandler.js';

let dataFromAPI;
const newsUrl = "http://127.0.0.1:8000/api/news/";

export function DetailedNewsController(id) {

    return new Promise((resolve, reject) => {
        resolve(requester.getJSON(newsUrl + id + '/'));
    }).then((newData) => {
        dataFromAPI = newData;
        return new Promise((resolve, reject) => {
            resolve(templates.get('detailed-news'));
        });
    }).then((res) => {
        let hbTemplate = Handlebars.compile(res),
            template = hbTemplate(dataFromAPI);

        $('#content').html(template);

        formHandler();

        $('#add-comment-button').on('click', () => {
            let body = {
                content: ''
            },
                addCommentUrl = `http://127.0.0.1:8000/api/news/${id}/comments/`;

            if (validator.comment($('#comment-content').val())) {
                body.content = $('#comment-content').val();
                requester.postJSON(addCommentUrl, body)
                    .then(() => {
                        toastr.success('Comment added!');
                        $('#comment-content').val('');
                    }).catch((err) => {
                        toastr.error('Comments can\' be empty!')
                    })
            }
            else {
                toastr.error('Comments shold be max 2048 characters long!');
            }
        });
    }).catch((err) => {
        console.log(err);
    });

}

export function loadComments(id) {
    let getData = requester.getJSON(newsUrl + id + '/'),
        getTemplate = templates.get('partials/comment');

    Promise.all([getData, getTemplate]).then((result) => {
        let newData = result[0],
            hbTemplate = Handlebars.compile(result[1]),
            commentsToLoad = [];

        commentsToLoad = newData.comment_set.filter(function (obj) {
            return !dataFromAPI.comment_set.some(function (obj2) {
                return obj.content === obj2.content && obj.posted_by.user === obj2.posted_by.user;
            });
        });

        dataFromAPI.comment_set = newData.comment_set;

        for (let i = 0; i < commentsToLoad.length; i += 1) {
            let template = hbTemplate(commentsToLoad[i]);
            $('#comments').append(template);
        }
    })
}
