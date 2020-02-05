export class Credentials {
    username: string;
    password: string;
    constructor(
        username: string,
        password: string
    ) {
        this.username = username;
        this.password = password;
    }
}

export class Tokens {
    access: string;
    refresh?: string;
    constructor(
        access: string,
        refresh?: string
    ) {
        this.access = access;
        this.refresh = refresh;
    }
}

export class ProfileInfo {
    id: string;
    fullName: string;
    givenName: string;
    familyName: string;
    imageURL: string;
    email: string;
    constructor(
        id: string,
        fullName: string,
        givenName: string,
        familyName: string,
        imageURL: string,
        email: string,
    ) {
        this.id = id;
        this.fullName = fullName;
        this.givenName = givenName;
        this.familyName = familyName;
        this.imageURL = imageURL;
        this.email = email;
    }
}

export class IdToken {
    idToken: string;
    email: string;
    constructor(
        idToken: string,
        email: string,
    ) {
        this.idToken = idToken;
        this.email = email;
    }
}

export class LoginTokens {
    token: string;
    constructor(
        token: string
    ) {
        this.token = token;
    }
}

export class User {
    url: string;
    username: string;
    email: string;
    isStaff: boolean;
    constructor(
        url: string,
        username: string,
        email: string,
        isStaff: boolean,
    ) {
        this.url = url;
        this.username = username;
        this.email = email;
        this.isStaff = isStaff;
    }
}

export class Test {
    title: string;
    result: boolean;
    constructor(
        title: string,
        result: boolean,
    ) {
        this.title = title;
        this.result = result;
    }
}
