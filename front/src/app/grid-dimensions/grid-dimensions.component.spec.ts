import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GridDimensionsComponent } from './grid-dimensions.component';

describe('GridDimensionsComponent', () => {
  let component: GridDimensionsComponent;
  let fixture: ComponentFixture<GridDimensionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GridDimensionsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GridDimensionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
