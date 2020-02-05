import { TestBed } from '@angular/core/testing';
import { Upload } from './upload.classes';

describe('Upload model', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const desiredName = 'name';
    const nameFlag = 'name';
    const configFile = 'config';
    const model: Upload = new Upload(
      desiredName,
      nameFlag,
      configFile,
    );
    expect(model).toBeTruthy();
  });
});
