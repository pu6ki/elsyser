import { requester } from '../../utils/requster.js';
import { templates } from '../../utils/templates.js';

let dataFromAPI;
let newsUrl = "http://127.0.0.1:8000/api/news/";

export function DetailedNewsController(id) {
    return new Promise((resolve, reject) => {
        resolve(requester.getJSON(newsUrl + id + '/'));
    }).then((data) => {
        dataFromAPI = data;
        return new Promise((resolve, reject) => {
            resolve(templates.get('detailed-news'));
        });
    }).then((res) => {
        let hbTemplate = Handlebars.compile(res),
            template = hbTemplate(dataFromAPI);
        $('#content').html(template);
    }).catch((err) => {
        console.log(err);
    });


}

export function loadNews(id) {
    console.log('req');
    requester.getJSON(newsUrl + id + '/')
        .then((data) => {
            if (data.comment_set.length > dataFromAPI.comment_set.length) {
                templates.get('partials/comment')
                    .then((res) => {
                        let hbTemplate = Handlebars.compile(res),
                            template = hbTemplate(data.comment_set[dataFromAPI.comment_set.length]);
                        $('#comments').append(template);
                        dataFromAPI = data;
                    });
            }
        });
}