import { Component, Output, EventEmitter } from '@angular/core';
import {NgClass} from "@angular/common";

@Component({
  selector: 'app-color-buttons',
  imports: [
    NgClass
  ],
  templateUrl: './color-buttons.component.html',
  standalone: true,
  styleUrls: ['./color-buttons.component.css']
})
export class ColorButtonsComponent {
  @Output() colorChange = new EventEmitter<string>();
  selectedColor: string = 'black'; // Noir pré-sélectionné par défaut

  changeColor(color: string): void {
    this.selectedColor = color;
    this.colorChange.emit(color);
  }

  isColorUsed(color: string): boolean {
    return this.selectedColor === color;
  }
}