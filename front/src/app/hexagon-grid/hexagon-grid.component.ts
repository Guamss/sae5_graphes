import { Component, OnInit, Input, OnChanges, SimpleChanges } from '@angular/core';
import { NgForOf } from '@angular/common';
import { Grid } from "../model/grid";

@Component({
  selector: 'app-hexagon-grid',
  templateUrl: './hexagon-grid.component.html',
  standalone: true,
  imports: [
    NgForOf
  ],
  styleUrls: ['./hexagon-grid.component.css']
})
export class HexagonGridComponent implements OnInit, OnChanges {
  @Input() grid: Grid | undefined;

  calculatedPositions: { x: number, y: number }[] = [];

  constructor() { }

  ngOnInit(): void {
    this.calculatePositions();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['grid'] && this.grid) {
      this.calculatePositions();  // Recalculer les positions si grid change
    }
  }

  calculatePositions(): void {
    const width = this.grid?.width || 0;
    const height = this.grid?.height || 0;

    const startX = 35; // Coordonnée de départ X
    const startY = 41; // Coordonnée de départ Y
    const spacingX = 15; // Espacement entre les "pods"
    const spacingY = 18; // Espacement entre les "pods"

    this.calculatedPositions = [];

    // Parcours de la largeur (hauteur du grid)
    for (let j = 0; j < height; j++) {
      // Parcours de la longueur (largeur du grid)
      for (let i = 0; i < width; i++) {
        const x = startX + i * spacingX; // Déplacement en X
        const y = startY + (j * spacingY) + (i % 2 === 0 ? 0 : spacingY / 2); // Ajustement en Y pour créer l'effet décalé

        this.calculatedPositions.push({ x, y });
      }
    }
  }
}
