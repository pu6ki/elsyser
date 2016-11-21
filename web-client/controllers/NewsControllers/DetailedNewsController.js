import { requester } from '../../utils/requster.js';
import { templates } from '../../utils/templates.js';
import { validator } from '../../utils/validator.js';
import { formHandler } from '../../utils/formHandler.js';

import { EditNewsController } from './EditNewsController.js';
import { DeleteNewsController } from './DeleteNewsController.js';

import { AddCommentController } from './AddCommentController.js';
import { EditCommentController } from './EditCommentController.js';
import { DeleteCommentController } from './DeleteCommentController.js';


let dataFromAPI, currentUsername;
const newsUrl = "http://127.0.0.1:8000/api/news/";

export function DetailedNewsController(id) {
    currentUsername = localStorage.getItem('elsyser-username');
    let getData = requester.getJSON(newsUrl + id + '/'),
        getTemplate = templates.get('detailed-news');

    Promise.all([getData, getTemplate])
        .then((result) => {
            dataFromAPI = result[0];
            let hbTemplate = Handlebars.compile(result[1]),
                newsId = dataFromAPI.id;

            if (dataFromAPI.author.user === currentUsername) {
                dataFromAPI.editable = true;
            }

            dataFromAPI.comment_set.reverse();

            dataFromAPI.comment_set.forEach((el) => {
                if (el.posted_by.user === currentUsername) {
                    el.editableComment = true;
                    $('#content').html(hbTemplate(dataFromAPI));

                    let commentId = el.id;

                    $(document).on('click', `#news-${newsId}-edit-comment-${commentId}`, () => {
                        EditCommentController(newsId, commentId);
                    })

                    $(document).on('click', `#news-${newsId}-delete-comment-${commentId}`, () => {
                        DeleteCommentController(newsId, commentId);
                    })
                }
            });


            let template = hbTemplate(dataFromAPI);
            $('#content').html(template);

            $(`#news-${newsId}-edit`).on('click', () => {
                EditNewsController(newsId);
            })

            $(`#news-${newsId}-delete`).on('click', () => {
                DeleteNewsController(newsId);
            })

            $('.new-comment').removeClass('new-comment');

            formHandler();

            $(".comment").slice(0, 2).show();
            $("#loadMore").on('click', () => {
                $(".comment:hidden").slice(0, 5).slideDown();
                if ($("div:hidden").length === 0) {
                    $("#loadMore").fadeOut('slow');
                }
            });

            $('.toTop').click(function () {
                $('body,html').animate({
                    scrollTop: 0
                }, 600);
                return false;
            });

            $('#add-comment-button').on('click', () => {
                AddCommentController(id);
            });

        }).catch((err) => {
            console.log(err);
        });
}

export function loadComments(newsId) {
    let getData = requester.getJSON(newsUrl + newsId + '/'),
        getTemplate = templates.get('partials/comment');

    Promise.all([getData, getTemplate]).then((result) => {
        let newData = result[0],
            hbTemplate = Handlebars.compile(result[1]),
            commentsToLoad = [];

        newData.comment_set.reverse();

        commentsToLoad = newData.comment_set.filter(function (obj) {
            return !dataFromAPI.comment_set.some(function (obj2) {
                return obj.id === obj2.id;
            });
        });

        dataFromAPI.comment_set = newData.comment_set;

        for (let i = 0; i < commentsToLoad.length; i += 1) {
            if (commentsToLoad[i].posted_by.user == currentUsername) {
                commentsToLoad[i].newsId = newsId;
                commentsToLoad[i].editable = true;
            }
            let template = hbTemplate(commentsToLoad[i]);
            $('#comments').prepend(template);

            $(document).on('click', `#news-${newsId}-edit-comment-${commentsToLoad[i].id}`, () => {
                EditCommentController(newsId, commentsToLoad[i].id);
            })

            $(document).on('click', `#news-${newsId}-delete-comment-${commentsToLoad[i].id}`, () => {
                DeleteCommentController(newsId, commentsToLoad[i].id);
            })
        }
    });
}
