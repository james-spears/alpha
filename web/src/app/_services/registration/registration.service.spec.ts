import { TestBed, getTestBed } from '@angular/core/testing';

import { RegistrationService } from './registration.service';

import { 
  HttpClientTestingModule, HttpTestingController 
} from '@angular/common/http/testing';

import { 
  Registration
} from '../../_models/registration/registration.classes';

describe('RegistrationService', () => {
  let injector: TestBed;
  let service: RegistrationService;
  let httpMock: HttpTestingController;
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule
      ],
      providers: [
        RegistrationService
      ]
    });
    // inject http service and test controller for
    // each test
    injector = getTestBed();
    service = injector.get(RegistrationService);
    httpMock = injector.get(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should register a user', () => {
    const registration = new Registration(
      'user',
      'email',
      'pass',
      'pass'
    );

    const mockResponse = {
      "status": "ok"
    }
    
    // login the mock user
    service.register(
      registration.username,
      registration.email,
      registration.password1,
      registration.password2
    ).subscribe(response => {

      // expect mock response to proivde mockReponse 
      expect(response).toEqual(mockResponse);
    });
    const req = httpMock.expectOne(
      `${service.getUrl()}/auth/registration/`);
    expect(req.request.method).toBe("POST");
    req.flush(mockResponse);
  });
});
