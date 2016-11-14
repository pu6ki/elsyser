import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';

export function ExamsController() {
    let examsUrl = 'http://127.0.0.1:8000/api/exams/',
        getData = requester.getJSON(examsUrl),
        getTemplate = templates.get('exams');

    Promise.all([getData, getTemplate])
        .then((result) => {
            let data = result[0],
                hbTemplate = Handlebars.compile(result[1]),
                template = hbTemplate(data);

            $('#content').html(template);
        }).catch((err) => {
            console.log(err);
        });
}