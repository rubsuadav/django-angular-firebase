import { TestBed } from '@angular/core/testing';

import { PostService as pService } from './post.service';

describe('PostService', () => {
  let service: pService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(pService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
