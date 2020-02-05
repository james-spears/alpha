import { TestBed } from '@angular/core/testing';
import { 
    Credentials,
    Tokens, 
    User, 
    Test,
    LoginTokens
} from './auth.classes';

describe('Credentials model', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const username = 'user';
    const password = 'pass';
    const model: Credentials = new Credentials(
        username,
        password
    );
    expect(model).toBeTruthy();
  });
});

describe('Tokens model', () => {
    beforeEach(() => TestBed.configureTestingModule({}));
  
    it('should be created', () => {
      const access = 'access';
      const refresh = 'refresh';
      const model: Tokens = new Tokens(
          access,
          refresh
      );
      expect(model).toBeTruthy();
    });
  });

  describe('LoginTokens model', () => {
    beforeEach(() => TestBed.configureTestingModule({}));
  
    it('should be created', () => {
      const token = 'token';
      const model: LoginTokens = new LoginTokens(
          token
      );
      expect(model).toBeTruthy();
    });
  });

describe('User model', () => {
    beforeEach(() => TestBed.configureTestingModule({}));
  
    it('should be created', () => {
      const url = 'url';
      const username = 'username';
      const email = 'email';
      const isStaff = true;
      const model: User = new User(
          url,
          username,
          email,
          isStaff
      );
      expect(model).toBeTruthy();
    });
  });

describe('Test model', () => {
    beforeEach(() => TestBed.configureTestingModule({}));
  
    it('should be created', () => {
        const title = 'title';
        const result = true;
        const model: Test = new Test(
            title,
            result
        );
      expect(model).toBeTruthy();
    });
  });
