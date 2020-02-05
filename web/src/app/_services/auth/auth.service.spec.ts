import { TestBed, getTestBed } from '@angular/core/testing';

import { AuthService } from './auth.service';

import { 
  HttpClientTestingModule, HttpTestingController 
} from '@angular/common/http/testing';

import { 
  Credentials,
  Tokens
} from '../../_models/auth/auth.classes';

describe('AuthService', () => {
  let injector: TestBed;
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule
      ],
      providers: [
        AuthService
      ]
    });
    // inject http service and test controller for
    // each test
    injector = getTestBed();
    service = injector.get(AuthService);
    httpMock = injector.get(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should log in a user', () => {
    const credentials = new Credentials(
      'user',
      'pass'
    );

    const mockTokens = new Tokens(
      'access',
      'refresh'
    );
    
    // login the mock user
    service.login(
      credentials.username,
      credentials.password
    ).subscribe(tokens => {

      // expect mock response to proivde mock tokens 
      expect(tokens).toEqual(mockTokens);

      // expect the currentTokensValue method to return
      // current tokens from local storage
      expect(service.currentTokensValue()).toEqual(mockTokens);

      // log out the mock user
      service.logout();

      // check that mock tokens were reomved from
      // local storage
      expect(service.currentTokensValue()).toEqual(null);
    });

    const req = httpMock.expectOne(`${service.getUrl()}/login/token/`);
    expect(req.request.method).toBe("POST");
    req.flush(mockTokens);
  });
});
