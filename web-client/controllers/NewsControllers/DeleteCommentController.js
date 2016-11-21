import { requester } from '../../utils/requster.js';
import { DetailedNewsController } from './DetailedNewsController.js';

export function DeleteCommentController(newsId, commentId) {
    let commentToDeleteUrl = `http://127.0.0.1:8000/api/news/${newsId}/comments/${commentId}/`;

    if (confirm("Are you sure you want to delete this comment?")) {
        Promise.resolve(requester.delete(commentToDeleteUrl))
            .then(() => {
                toastr.success('Comment deleted successfully!');
            }).catch((err) => {
                toastr.error('Couldn\'t delete the selected comment!');
            });

        DetailedNewsController(newsId);
    }
}