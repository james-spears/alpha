import { Injectable, isDevMode } from '@angular/core';
import { 
  HttpClient,
  HttpHeaders 
} from '@angular/common/http';
import { map } from 'rxjs/operators';

import { 
  Registration 
} from '../../_models/registration/registration.classes';

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
export class RegistrationService {

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

  register(
    username: string, 
    email: string, 
    password1: string, 
    password2: string) {
    return this.http.post<any>(
      `${this.getUrl()}/auth/registration/`, 
      new Registration(
        username, 
        email, 
        password1, 
        password2
        ), 
        httpOptions
      ).pipe(map(response => {
            return response;
        }));
      }
}
