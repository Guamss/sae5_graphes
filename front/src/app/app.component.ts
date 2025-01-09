import { Component } from '@angular/core';
import {HexagonGridComponent} from './hexagon-grid/hexagon-grid.component';
import {ColorButtonsComponent} from "./color-buttons/color-buttons.component";
import {ActionButtonsComponent} from "./action-buttons/action-buttons.component";
import {GridDimensionsComponent} from "./grid-dimensions/grid-dimensions.component";

@Component({
  selector: 'app-root',
  imports: [HexagonGridComponent, ColorButtonsComponent, ActionButtonsComponent, GridDimensionsComponent],
  templateUrl: './app.component.html',
  standalone: true,
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'chiffredeux';
}
