import { Injectable, isDevMode } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Upload } from '../../_models/upload/upload.classes';
// import { stringify } from 'querystring';

const httpOptions = {
  headers: new HttpHeaders(
    { 
      'Content-Type': 'application/json' 
    }
  )
};


@Injectable({
  providedIn: 'root'
})
export class UploadService {

  constructor(
    private http: HttpClient,
  ) { }

  getUrl() {
    
    if (isDevMode()) {
      return 'http://127.0.0.1:8000/api/v1';
    } else {
      return 'https://alpha.example.com/api/v1';
    }
  
  }

  uploadFile(
    desiredName: string,
    fileType: string,
    file: string,
    ) {
    return this.http.post<any>(
      `${this.getUrl()}/stt/`,
      new Upload(
        desiredName,
        fileType,
        file,
        ), 
        httpOptions
        ).pipe(map(response => {
              return response;
          }));
  }
}