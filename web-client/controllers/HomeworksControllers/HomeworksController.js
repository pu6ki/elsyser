import { requester } from '../../utils/requster.js';
import { templates } from '../../utils/templates.js';

export function HomeworksController() {
    let dataFromAPI;
    return new Promise((resolve, reject) => {
        let examsUrl = 'http://127.0.0.1:8000/api/homeworks/';

        resolve(requester.getJSON(examsUrl));
    }).then((data) => {
        dataFromAPI = data;
        return new Promise((resolve, reject) => {
            resolve(templates.get('homeworks'));
        });
    }).then((res) => {
        let hbTemplate = Handlebars.compile(res),
            template = hbTemplate(dataFromAPI);
        $('#content').html(template);
    }).catch((err) => {
        console.log(err);
    });
}