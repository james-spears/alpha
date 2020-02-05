import { 
    Injectable 
} from '@angular/core';

import { 
    HttpRequest, 
    HttpHandler, 
    HttpEvent, 
    HttpInterceptor 
} from '@angular/common/http';

import { 
    Observable 
} from 'rxjs';

import { 
    AuthService 
} from '../_services/auth/auth.service';

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
    constructor(
        private authService: AuthService,
        ) { }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        // add authorization header with jwt token if available
        const currentTokens = this.authService.currentTokensValue();
        // console.log(currentTokens)
        if (currentTokens && currentTokens.access && currentTokens.refresh) {
            request = request.clone({
                setHeaders: {
                    Authorization: `Bearer ${currentTokens.access}`,
                }
            });
            // console.log(request)
        }
        return next.handle(request);
    }
}
