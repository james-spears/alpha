import { TestBed, getTestBed } from '@angular/core/testing';

import { SupportService } from './support.service';

import { 
  HttpClientTestingModule, HttpTestingController 
} from '@angular/common/http/testing';

import { SupportRequest } from '../../_models/support/support.classes';

describe('AuthService', () => {
  let injector: TestBed;
  let service: SupportService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule
      ],
      providers: [
        SupportService
      ]
    });
    // inject http service and test controller for
    // each test
    injector = getTestBed();
    service = injector.get(SupportService);
    httpMock = injector.get(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should log in a user', () => {
    const supportRequest = new SupportRequest(
      'you@example.com',
      'content'
    );

    const mockResponse = {
      "status": "ok"
    };

    // login the mock user
    service.supportRequest(
      supportRequest.email,
      supportRequest.content
    ).subscribe(response => {
      // expect mock response to proivde mock response 
      expect(response).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${service.getUrl()}/support/request/`);
    expect(req.request.method).toBe("POST");
    req.flush(mockResponse);

  });
});