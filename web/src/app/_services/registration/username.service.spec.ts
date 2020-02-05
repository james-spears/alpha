import { TestBed, getTestBed } from '@angular/core/testing';

import { UsernameService } from './username.service';

import { 
  HttpClientTestingModule, HttpTestingController 
} from '@angular/common/http/testing';

describe('UsernameService', () => {
  let injector: TestBed;
  let service: UsernameService;
  let httpMock: HttpTestingController;
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule
      ],
      providers: [
        UsernameService
      ]
    });
    // inject http service and test controller for
    // each test
    injector = getTestBed();
    service = injector.get(UsernameService);
    httpMock = injector.get(HttpTestingController);
  });
  
  afterEach(() => {
      httpMock.verify();
    });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should return a user if they exist', () => {
    const mockResponse = [{
      "username": "user"
    }];

    const username = 'user';

    // login the mock user
    service.checkUsername(
      username
    ).subscribe(tokens => {

      // expect mock response to proivde mock user
      expect(tokens).toEqual(mockResponse);

    });

    const req = httpMock.expectOne(`${service.getUrl()}/user/?search=${username}`);
    expect(req.request.method).toBe("GET");
    req.flush(mockResponse);

  });

  it('should return a * if search field is blank', () => {
    const mockResponse = [];

    const username = '*';

    // login the mock user
    service.checkUsername().subscribe(tokens => {

      // expect mock response to proivde mock user
      expect(tokens).toEqual(mockResponse);

    });

    const req = httpMock.expectOne(`${service.getUrl()}/user/?search=${username}`);
    expect(req.request.method).toBe("GET");
    req.flush(mockResponse);

  });

});
