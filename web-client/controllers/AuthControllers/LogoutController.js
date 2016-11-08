export function LogoutController() {
    toastr.success('Logged-out successfully!');
    window.localStorage.removeItem('token');
    window.location.href = '#/home';
}
