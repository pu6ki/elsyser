export function LogoutController() {
    toastr.success('Logged-out successfully!');
    localStorage.removeItem('token');
    localStorage.removeItem('elsyser-username');
    window.location.href = '#/home';
}
