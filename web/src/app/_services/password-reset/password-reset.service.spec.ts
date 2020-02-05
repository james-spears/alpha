import { 
  TestBed,
  getTestBed 
} from '@angular/core/testing';

import { 
  PasswordResetService 
} from './password-reset.service';

import { 
  HttpClientTestingModule,
  HttpTestingController 
} from '@angular/common/http/testing';

describe('PasswordResetService', () => {
  let injector: TestBed;
  let service: PasswordResetService;
  let httpMock: HttpTestingController;
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule
      ],
      providers: [
        PasswordResetService
      ]
    });
    // inject http service and test controller for
    // each test
    injector = getTestBed();
    service = injector.get(PasswordResetService);
    httpMock = injector.get(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should reset a password', () => {
    const pass = 'pass';
    const uid = 'uid';
    const token = 'token';

    const mockResponse = {
      "status": "ok"
    };

    // login the mock user
    service.reset(
      pass,
      pass,
      uid,
      token
    ).subscribe(response => {
      // expect mock response to proivde mock response 
      expect(response).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(
      `${service.getUrl()}/auth/password/reset/confirm/`
      + `${uid}/${token}`);
    expect(req.request.method).toBe("POST");
    req.flush(mockResponse);

  });

});
