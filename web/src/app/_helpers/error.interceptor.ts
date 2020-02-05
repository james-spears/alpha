import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';

import { AuthService } from '../_services/auth/auth.service';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
    constructor(
        private authService: AuthService,
        private router: Router,
        ) { }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        return next.handle(request).pipe(catchError(err => {
            if (err.status === 401) {
                // auto logout if 401 response returned from api
                // unless the requested end points are returned
                // 401 unauthorized the user will be able to view
                // the requested page
                this.authService.logout();
                this.router.navigate(['ui/auth']);
                const error = err.error.message || err.statusText;
                return throwError(error);
            } else if (err.status !== 200) {
                const error = err.error;
                return throwError(error);
            }
        }));
    }
}
