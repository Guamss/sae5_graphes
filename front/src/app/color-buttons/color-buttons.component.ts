import { Component } from '@angular/core';

@Component({
  selector: 'app-color-buttons',
  imports: [],
  templateUrl: './color-buttons.component.html',
  standalone: true,
  styleUrl: './color-buttons.component.css'
})
export class ColorButtonsComponent {
    selectedColor: string = "black";
    changeColor(color: string): void {
    this.selectedColor = color;
  }
}
