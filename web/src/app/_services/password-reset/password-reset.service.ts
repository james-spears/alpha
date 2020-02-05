import { Injectable, isDevMode } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { PasswordReset } from '../../_models/password-reset/password-reset.classes';


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
export class PasswordResetService {

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

  reset(
    newPassword1: string,
    newPassword2: string,
    uid: string,
    token: string
    ) {
    const post = new  PasswordReset(
      newPassword1,
      newPassword2,
      uid,
      token
    );
    return this.http.post<any>(
      `${this.getUrl()}/auth/password/reset/confirm/`
      +`${uid}/${token}`, post, httpOptions)
        .pipe(map(response => {
            return response;
        }));
  }

}
