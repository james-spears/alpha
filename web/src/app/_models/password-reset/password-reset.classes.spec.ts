import { TestBed } from '@angular/core/testing';
import { PasswordReset } from './password-reset.classes';

describe('PasswordReset model', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const newPassword1 = 'pass';
    const newPassword2 = 'pass';
    const uuid = 'uuid';
    const token = 'token';
    const model: PasswordReset = new PasswordReset(
        newPassword1,
        newPassword2,
        uuid,
        token
    );
    expect(model).toBeTruthy();
  });
});
