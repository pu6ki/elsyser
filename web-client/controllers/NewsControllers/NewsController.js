import { requester } from '../../utils/requster.js';
import { templates } from '../../utils/templates.js';

const newsUrl = 'http://127.0.0.1:8000/api/news/';
const currentUsername = localStorage.getItem('elsyser-username');

export function NewsController() {
    let data,
        getData = requester.getJSON(newsUrl),
        getTemplate = templates.get('news');

    Promise.all([getData, getTemplate])
        .then((result) => {
            let newData = result[0],
                hbTemplate = Handlebars.compile(result[1]);

            data = newData;
            data.forEach((el) => {
                if (el.comment_set.length > 0) {
                    el.comments_count = el.comment_set.length;
                }
                if (el.author.user === currentUsername) {
                    el.editable = true;
                }
            }, this);

            let template = hbTemplate(data);
            $('#content').html(template);
        }).catch((err) => {
            console.log(err);
        });
}
