import { requester } from '../../utils/requster.js';
import { templates } from '../../utils/templates.js';
import { validator } from '../../utils/validator.js';
import { formHandler } from '../../utils/formHandler.js';

let commentToEditUrl;

export function EditCommentController(newsId, commentId) {
        commentToEditUrl = `http://127.0.0.1:8000/api/news/${newsId}/comments/${commentId}/`;
        let getData = requester.getJSON(commentToEditUrl),
        getTemplate = templates.get('edit-comment');

    Promise.all([getData, getTemplate])
        .then((result) => {
            let data = result[0],
                hbTemplate = Handlebars.compile(result[1]),
                template = hbTemplate(data);

            $(`#comment-${commentId}`).html(template);

            formHandler();

            $('#save-button').on('click', () => {
                editData(newsId, commentId);
            });
        });
}

function editData(newsId, commentId) {
    let body = {
        content: '',
        edited: true
    };

    if (validator.comment($('#new-comment-content').val())) {
        body.content = $('#new-comment-content').val();
    }
    else {
        toastr.error('Couldn\'t edit the comment! It should have maximum length of 2048 characters!');
        return;
    }

    requester.putJSON(commentToEditUrl, body)
        .then(() => {
            toastr.success('Comment updated successfully!');
            window.location.href = `#/news/${newsId}`;
        }).catch(() => {
            toastr.error('Couldn\'t edit the comment!');
            window.location.href = `#/news/${newsId}`;
        });
}
