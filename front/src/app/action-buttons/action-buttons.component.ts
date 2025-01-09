import { Component } from '@angular/core';

@Component({
  selector: 'app-action-buttons',
  imports: [],
  templateUrl: './action-buttons.component.html',
  standalone: true,
  styleUrl: './action-buttons.component.css'
})
export class ActionButtonsComponent {


  generateGrid() {
    console.log("generateGrid")
  }

  setStartMode() {
    console.log("setStartMode")
  }

  setEndMode() {
    console.log("setEndMode")
  }
}
