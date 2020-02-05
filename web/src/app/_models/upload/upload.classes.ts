export class Upload {
    desiredName: string;
    fileType: string;
    fileContents: string;
    constructor(
        desiredName: string,
        fileType: string,
        fileContents: string,
    ) {
        this.desiredName = desiredName;
        this.fileType = fileType;
        this.fileContents = fileContents;
    }
}