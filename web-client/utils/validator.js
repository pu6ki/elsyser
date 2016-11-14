export let validator = {
    email: (email) => {
        let regexPattern = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
        return regexPattern.test(email);
    },
    name: (name) => {
        if (typeof name === 'string') {
            if (name.length >= 3 && name.length <= 30) {
                return true;
            }
        }
        return false;
    },
    password: (password) => {
        // Password should contain atleast one number and one special character and capital letter and be between 6 and 16 symbols long
        let regexPattern = /^(?=.*[0-9])[a-zA-Z0-9!]{6,16}$/;
        return regexPattern.test(password);
    },
    title: (title) => {
        if (typeof title === 'string') {
            if (title.length >= 3 && title.length <= 60) {
                return true;
            }
        }
        return false;
    },
    content: (content) => {
        if (typeof content === 'string') {
            if (content.length >= 5 && content.length <= 1000) {
                return true;
            }
        }
        return false;
    },
    comment: (comment) => {
        if (typeof comment === 'string') {
            if (comment.length >= 1 && comment.length <= 2048) {
                return true;
            }
        }
        return false;
    }
};
