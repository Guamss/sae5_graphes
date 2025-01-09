import {Component} from '@angular/core';
import {HexagonGridComponent} from './hexagon-grid/hexagon-grid.component';
import {ColorButtonsComponent} from "./color-buttons/color-buttons.component";
import {ActionButtonsComponent} from "./action-buttons/action-buttons.component";
import {GridDimensionsComponent} from "./grid-dimensions/grid-dimensions.component";
import {Grid} from "./model/grid";
import {GridService} from "./service/grid.service";

@Component({
  selector: 'app-root',
  imports: [HexagonGridComponent, ColorButtonsComponent, ActionButtonsComponent, GridDimensionsComponent],
  templateUrl: './app.component.html',
  standalone: true,
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'chiffredeux';
  currentGrid: Grid | undefined;

  constructor(private gridService: GridService) {}

  ngOnInit(): void {
    this.loadGridData();
  }

  loadGridData(): void {
    this.gridService.getGridWeights().subscribe({
      next: (weights) => {
        // Construire une grille avec les dimensions et les poids
        this.currentGrid = {
          height: weights.length,
          width: weights[0]?.length || 0,
          start: [0, weights.length-1], // Point de départ par défaut
          end: [weights[0]?.length - 1, 0], // Point d'arrivée par défaut
          tab: weights
        }; // Mise à jour de la grille actuelle
      },
      error: (err) => {
        console.error('Erreur lors du chargement des données de la grille:', err);
      }
    });
  }

  updateGrid(newGrid: Grid): void {
    this.currentGrid = { ...newGrid };
  }
}
