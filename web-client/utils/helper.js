import { requester } from './requster.js';

export function setUsernameToLocalSorage() {
    let profileUrl = 'http://127.0.0.1:8000/api/profile/';

    requester.getJSON(profileUrl)
        .then((data) => {
            localStorage.setItem('elsyser-username', data.user.username);
        });
}