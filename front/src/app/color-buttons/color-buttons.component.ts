import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-color-buttons',
  imports: [],
  templateUrl: './color-buttons.component.html',
  standalone: true,
  styleUrls: ['./color-buttons.component.css']
})
export class ColorButtonsComponent {
  @Output() colorChange = new EventEmitter<string>();

  changeColor(color: string): void {
    this.colorChange.emit(color);
  }
}