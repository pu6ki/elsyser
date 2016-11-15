import { requester } from '../utils/requster.js';
import { templates } from '../utils/templates.js';
import { validator } from '../utils/validator.js';

const profileUrl = 'http://127.0.0.1:8000/api/profile/';

export function EditProfileController() {
    let getData = requester.getJSON(profileUrl),
        getTemplate = templates.get('edit-profile');

    Promise.all([getData, getTemplate])
        .then((result) => {
            let data = result[0],
                hbTemplate = Handlebars.compile(result[1]),
                template = hbTemplate(data);

            $('#content').html(template);

            $('#save-button').on('click', () => {
                editData();
            });
        });
}

function editData() {
    let body = {
        user: {
            first_name: '',
            last_name: ''
        }
    };

    if (validator.name($('#new-first-name').val())) {
        body.user.first_name = $('#new-first-name').val();
    }
    else {
        toastr.error('First Name shoud be between 3 and 30 characters long!');
        return;
    }
    if (validator.name($('#new-last-name').val())) {
        body.user.last_name = $('#new-last-name').val();
    }
    else {
        toastr.error('Last Name shoud be between 3 and 30 characters long!');
        return;
    }

    requester.putJSON(profileUrl, body)
        .then(() => {
            toastr.success('Data updated successfully!');
            window.location.href = '#/profile';
        });
}

//TODO: Edit profile picture
// function editProfilePicture() {
//     let body = {
//         profile_image: new FormData($('#new-profile-picture').prop('files')) 
//     };

//     Promise.resolve(requester.putImage(profileUrl, body)); 
// }