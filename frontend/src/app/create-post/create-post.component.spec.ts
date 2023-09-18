import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreatePostComponent as create } from './create-post.component';

describe('CreatePostComponent', () => {
  let component: create;
  let fixture: ComponentFixture<create>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [create],
    });
    fixture = TestBed.createComponent(create);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
