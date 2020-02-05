import { TestBed } from '@angular/core/testing';
import { 
    Registration,
    Username
} from './registration.classes';

describe('Registration model', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const username = 'user';
    const email = 'email';
    const password1 = 'pass';
    const password2 = 'pass';
    const model: Registration = new Registration(
        username,
        email,
        password1,
        password2
    );
    expect(model).toBeTruthy();
  });
});

describe('Username', () => {
    beforeEach(() => TestBed.configureTestingModule({}));
  
    it('should be created', () => {
      const username = 'user';
      const model: Username = new Username(
          username
      );
      expect(model).toBeTruthy();
    });
  });
