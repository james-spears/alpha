import { Injectable, isDevMode } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { SupportRequest } from '../../_models/support/support.classes';

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
export class SupportService {


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

  supportRequest(email: string, content: string) {
    const post = new SupportRequest(
      email,
      content
    );
    return this.http.post<any>(`${this.getUrl()}/support/request/`, post, httpOptions)
        .pipe(map(response => {
            return response;
        }));
  }
}
