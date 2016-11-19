import { HeaderController } from '../HeaderController.js';

export function LogoutController() {
    toastr.success('Logged-out successfully!');
    localStorage.removeItem('token');
    localStorage.removeItem('elsyser-username');
    HeaderController();
    window.location.href = '#/home';
}
