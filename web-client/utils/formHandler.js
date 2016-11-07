export function formHandler() {
    $('.form-wrapper').on('keydown', (ev) => {
        if (ev.keyCode == 13) {
            $('.submit').trigger('click');
        }
    });
}