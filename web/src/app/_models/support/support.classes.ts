export class SupportRequest {
    email: string;
    content: string;
    constructor(
        email: string,
        content: string,
    ) {
        this.email = email;
        this.content = content;
    }
}