export function LogoutController() {
    window.localStorage.removeItem('token');
    toastr.success('Logged-out successfully!');
    window.location.href = '#/home';
    window.location.reload(true);
}