import { Component } from '@angular/core';
import { Grid } from './model/grid';
import { GridService } from './service/grid.service';
import {ActionButtonsComponent} from "./action-buttons/action-buttons.component";
import {ColorButtonsComponent} from "./color-buttons/color-buttons.component";
import {HexagonGridComponent} from "./hexagon-grid/hexagon-grid.component";
import {GridDimensionsComponent} from "./grid-dimensions/grid-dimensions.component";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: true,
  imports: [
    ActionButtonsComponent,
    ColorButtonsComponent,
    HexagonGridComponent,
    GridDimensionsComponent
  ],
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'chiffredeux';
  currentGrid: Grid | undefined;
  selectedColor: string = 'black'; // couleur de base

  constructor(private gridService: GridService) {}

  ngOnInit(): void {
    this.loadGridData();
  }

  loadGridData(): void {
    this.gridService.getGridWeights().subscribe({
      next: (weights) => {
        this.currentGrid = {
          height: weights.length,
          width: weights[0]?.length || 0,
          start: [weights[0]?.length - 1, 0], // Point d'arrivée par défaut
          end: [0, weights.length - 1], // Point de départ par défaut
          tab: weights
        };
      },
      error: (err) => {
        console.error('Erreur lors du chargement des données de la grille:', err);
      }
    });
  }

  updateGrid(newGrid: Grid): void {
    this.currentGrid = { ...newGrid };
  }

  onColorChange(color: string): void {
    this.selectedColor = color;
  }
}