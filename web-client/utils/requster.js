/* globals $ Promise */

let requester = {
    get(url, headers) {
        let promise = new Promise((resolve, reject) => {
            $.ajax({
                url,
                headers,
                method: "GET",
                success(response) {
                    resolve(response);
                },
                error(response) {
                    reject(response);
                }
            });
        });
        return promise;
    },
    putJSON(url, body, options = {}) {
        let promise = new Promise((resolve, reject) => {
            let headers = options.headers || {};
            $.ajax({
                url,
                headers,
                method: "PUT",
                contentType: "application/json",
                data: JSON.stringify(body),
                success(response) {
                    resolve(response);
                },
                error(response) {
                    throw Error(response);
                }
            });
        });
        return promise;
    },
    postJSON(url, body, options = {}) {
        let promise = new Promise((resolve, reject) => {
            let headers = options.headers || { };

            $.ajax({
                url,
                headers,
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify(body),
                crossDomain: true,
                success(response) {
                    resolve(response);
                },
                error(response) {
                    reject(response);
                }
            });
        });
        return promise;
    },
    getJSON(url, headers) {
        let promise = new Promise((resolve, reject) => {
            $.ajax({
                url,
                headers,
                method: "GET",
                contentType: "application/json",
                success(response) {
                    resolve(response);
                },
                error(response) {
                    reject(response);
                }
            });
        });
        return promise;
    }
};

export { requester };