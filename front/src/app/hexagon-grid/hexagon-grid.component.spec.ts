import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HexagonGridComponent } from './hexagon-grid.component';

describe('ColorButtonsComponent', () => {
  let component: HexagonGridComponent;
  let fixture: ComponentFixture<HexagonGridComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HexagonGridComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HexagonGridComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
