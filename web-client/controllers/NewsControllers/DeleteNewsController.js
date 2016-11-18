import { requester } from '../../utils/requster.js';

const newsUrl = 'http://127.0.0.1:8000/api/news/';

export function DeleteNewsController(id) {
    let deleteNewsUrl = newsUrl + id + '/';

    if (confirm("Are you sure you want to delete this news?")) {
        requester.delete(deleteNewsUrl)
            .then(() => {
                toastr.success('Deleted successfully!');
                window.location.href = "#/news";
            }).catch(() => {
                toastr.error('Can\'t delete the selected news!');
            });
    }
}