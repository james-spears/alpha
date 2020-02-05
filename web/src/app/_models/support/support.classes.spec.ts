import { TestBed } from '@angular/core/testing';
import { SupportRequest } from './support.classes';

describe('Content model', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const content = 'content';
    const email = 'you@example.com'
    const model: SupportRequest = new SupportRequest(
        email,
        content
    );
    expect(model).toBeTruthy();
    expect(model.content).toContain('content');
    expect(model.email).toContain('you@example.com')
  });
});
