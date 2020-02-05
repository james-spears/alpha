export class PasswordReset {
    new_password1: string;
    new_password2: string;
    uid: string;
    token: string;
    constructor(
        newPassword1: string,
        newPassword2: string,
        uid: string,
        token: string,
    ) {
        this.new_password1 = newPassword1;
        this.new_password2 = newPassword2;
        this.uid = uid;
        this.token = token;
    }
}
