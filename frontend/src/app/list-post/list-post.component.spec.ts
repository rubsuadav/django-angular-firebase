import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListPostComponent as list } from './list-post.component';

describe('ListPostComponent', () => {
  let component: list;
  let fixture: ComponentFixture<list>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [list],
    });
    fixture = TestBed.createComponent(list);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
