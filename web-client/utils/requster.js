/* globals $ Promise */

let requester = {
    get(url) {
        let promise = new Promise((resolve, reject) => {
            $.ajax({
                url,
                method: "GET",
                beforeSend: (xhr) => {
                    let token = window.localStorage.getItem('token');
                    xhr.setRequestHeader('Authorization', `Token ${token}`);
                },
                success(response) {
                    return resolve(response);
                },
                error(response) {
                    return reject(response);
                }
            });
        });
        return promise;
    },
    putJSON(url, body, options = {}) {
        let promise = new Promise((resolve, reject) => {
            var headers = options.headers || {};
            $.ajax({
                url,
                headers,
                method: "PUT",
                contentType: "application/json",
                data: JSON.stringify(body),
                beforeSend: (xhr) => {
                    let token = window.localStorage.getItem('token');
                    xhr.setRequestHeader('Authorization', `Token ${token}`);
                },
                success(response) {
                    return resolve(response);
                },
                error(response) {
                    return reject(response);
                }
            });
        });
        return promise;
    },
    postJSON(url, body, options = {}) {
        let promise = new Promise((resolve, reject) => {
            var headers = options.headers || {};

            $.ajax({
                url,
                headers,
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify(body),
                crossDomain: true,
                beforeSend: (xhr) => {
                    let token = window.localStorage.getItem('token');
                    xhr.setRequestHeader('Authorization', `Token ${token}`);
                },
                success(response) {
                    return resolve(response);
                },
                error(response) {
                    return reject(response);
                }
            });
        });
        return promise;
    },
    getJSON(url) {
        let promise = new Promise((resolve, reject) => {
            $.ajax({
                url,
                method: "GET",
                contentType: "application/json",
                beforeSend: (xhr) => {
                    let token = window.localStorage.getItem('token');
                    xhr.setRequestHeader('Authorization', `Token ${token}`);
                },
                success(response) {
                    resolve(response);
                    return;
                },
                error(response) {
                    return reject(response);
                }
            });
        });
        return promise;
    },

    putImage(url, body, options) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url,
                method: "PUT",
                data: body.profile_image,
                beforeSend: (xhr) => {
                    let token = window.localStorage.getItem('token');
                    xhr.setRequestHeader('Authorization', `Token ${token}`);
                },
                success(response) {
                    return resolve(response);
                },
                error(response) {
                    return reject(response);
                }
            });
        });
    },

    delete(url) {
        let promise = new Promise((resolve, reject) => {
            $.ajax({
                url,
                method: "DELETE",
                beforeSend: (xhr) => {
                    let token = window.localStorage.getItem('token');
                    xhr.setRequestHeader('Authorization', `Token ${token}`);
                },
                success(response) {
                    return resolve(response);
                },
                error(response) {
                    return reject(response);
                }
            });
        });
        return promise;
    }
};

export { requester };