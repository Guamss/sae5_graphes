import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {HexagonGridComponent} from './hexagon-grid/hexagon-grid.component';

@Component({
  selector: 'app-root',
  imports: [HexagonGridComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'chiffredeux';
}
