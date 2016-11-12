import { requester } from '../../utils/requster.js';
import { templates } from '../../utils/templates.js';

const newsUrl = 'http://127.0.0.1:8000/api/news/';

export function NewsController() {
    let dataFromAPI;
    return new Promise((resolve, reject) => {
        resolve(requester.getJSON(newsUrl));
    }).then((data) => {
        dataFromAPI = data;
        dataFromAPI.forEach((el) => {
            if (el.comment_set.length > 0) {
                el.comments_count = el.comment_set.length;
            }
        }, this);
        return new Promise((resolve, reject) => {
            resolve(templates.get('news'));
        });
    }).then((res) => {
        let hbTemplate = Handlebars.compile(res),
            template = hbTemplate(dataFromAPI);
        $('#content').html(template);
    }).catch((err) => {
        console.log(err);
    });
}
