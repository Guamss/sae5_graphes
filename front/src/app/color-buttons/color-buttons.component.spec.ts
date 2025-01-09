import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ColorButtonsComponent } from './color-buttons.component';

describe('ColorButtonsComponent', () => {
  let component: ColorButtonsComponent;
  let fixture: ComponentFixture<ColorButtonsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ColorButtonsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ColorButtonsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
