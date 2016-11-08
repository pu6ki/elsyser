import { requester } from '../../utils/requster.js';
import { templates } from '../../utils/templates.js';

export function NewsController() {
    let dataFromAPI;
    return new Promise((resolve, reject) => {
        let newsUrl = 'http://127.0.0.1:8000/api/news/';

        resolve(requester.getJSON(newsUrl));
    }).then((data) => {
        dataFromAPI = data;
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
