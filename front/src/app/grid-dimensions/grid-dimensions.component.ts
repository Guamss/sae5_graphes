import {Component, EventEmitter, Output} from '@angular/core';
import {GridService} from "../service/grid.service";
import {FormsModule} from "@angular/forms";
import {NgIf} from "@angular/common";
import {Grid} from "../model/grid";

@Component({
  selector: 'app-grid-dimensions',
  imports: [
    FormsModule,
    NgIf
  ],
  templateUrl: './grid-dimensions.component.html',
  standalone: true,
  styleUrl: './grid-dimensions.component.css'
})
export class GridDimensionsComponent {
  width: number = 0;
  height: number = 0;
  message: string = '';

 @Output() gridUpdated = new EventEmitter<Grid>();

  constructor(private gridService: GridService) {}


  ngOnInit(): void {
    this.gridService.getGridDimensions().subscribe({
      next: (dimensions) => {
        this.height = dimensions.height;
        this.width = dimensions.width;
      },
      error: () => {
        this.message = 'Erreur lors de la récupération des dimensions de la grille.';
      }
    });
  }

  // Méthode pour envoyer les nouvelles dimensions à l'API
  sendGrid(): void {
    this.gridService.sendGridDimensions(this.height, this.width).subscribe({
      next: () => {
        this.message = 'Dimensions de la grille envoyées avec succès !';
        // Créer une nouvelle grille avec les dimensions mises à jour
        const updatedGrid: Grid = {
          width: this.width,
          height: this.height,
          start: [0, this.height - 1], // Ajuster les coordonnées de départ
          end: [this.width - 1, 0], // Ajuster les coordonnées d'arrivée
          tab: []
        };
        this.gridUpdated.emit(updatedGrid);  // Émettre l'événement avec la nouvelle grille
      },
      error: () => {
        this.message = 'Erreur lors de l\'envoi des dimensions.';
      }
    });
  }
}