import { Injectable, isDevMode } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Username } from '../../_models/registration/registration.classes';

@Injectable({ providedIn: 'root' })
export class UsernameService {

  constructor(
    private http: HttpClient
    ) { }

    getUrl() {
    
      if (isDevMode()) {
        return 'http://127.0.0.1:8000/api/v1';
      } else {
        return 'https://alpha.example.com/api/v1';
      }
    
    }

    checkUsername(username?: string) {
      if (username) {
        return this.http.get<Username[]>(`${this.getUrl()}/user/?search=${username}`);
      } else {
        return this.http.get<Username[]>(`${this.getUrl()}/user/?search=*`);
      }
  }
}
