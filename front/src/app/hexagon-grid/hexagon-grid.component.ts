import { Component, OnInit, Input, OnChanges, SimpleChanges, Output, EventEmitter } from '@angular/core';
import { NgForOf, NgClass } from '@angular/common';
import { Grid } from "../model/grid";

@Component({
  selector: 'app-hexagon-grid',
  templateUrl: './hexagon-grid.component.html',
  standalone: true,
  imports: [
    NgForOf,
    NgClass
  ],
  styleUrls: ['./hexagon-grid.component.css']
})
export class HexagonGridComponent implements OnInit, OnChanges {
  @Input() grid: Grid | undefined;
  @Input() selectedColor: string = 'black';

  calculatedPositions: { x: number, y: number }[] = [];
  isMouseDown: boolean = false;

  constructor() { }

  ngOnInit(): void {
    this.calculatePositions();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['grid'] && this.grid) {
      this.calculatePositions();
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

    for (let j = 0; j < height; j++) {
      for (let i = 0; i < width; i++) {
        const x = startX + i * spacingX;
        const y = startY + (j * spacingY) + (i % 2 === 0 ? 0 : spacingY / 2);
        this.calculatedPositions.push({ x, y });
      }
    }
  }

    changeHexagonColor(index: number): void {
    if (!this.grid) return;
    const row = Math.floor(index / this.grid.width);
    const col = index % this.grid.width;

    // Vérifie si l'index correspond à une position de départ
    if (this.isStart(index)) {
        alert("Vous ne pouvez pas écraser un départ !");
    }
    // Vérifie si l'index correspond à une position d'arrivée
    else if (this.isEnd(index)) {
        alert("Vous ne pouvez pas écraser une arrivée !");
    }
    // Si ce n'est ni un départ ni une arrivée, on peut modifier la couleur
    else {
        if (this.selectedColor === 'magenta') {
            this.grid.start = [col, row]; // Correction ici
        } else if (this.selectedColor === 'red') {
            this.grid.end = [col, row]; // Correction ici
        }
        this.grid.tab[row][col] = this.colorToNumber(this.selectedColor);
    }
  }


  getHexagonClass(index: number): string {
    if (!this.grid) return 'white';
    const row = Math.floor(index / this.grid.width);
    const col = index % this.grid.width;
    return this.numberToColor(this.grid.tab[row][col]);
  }

  getSvgViewBox(): string {
  if (!this.calculatedPositions.length) return '0 0 100 100'; // Valeurs par défaut si aucune position n'est calculée

  const minX = Math.min(...this.calculatedPositions.map(pos => pos.x)) - 20; // Ajout de marge
  const minY = Math.min(...this.calculatedPositions.map(pos => pos.y)) - 20;
  const maxX = Math.max(...this.calculatedPositions.map(pos => pos.x)) + 20;
  const maxY = Math.max(...this.calculatedPositions.map(pos => pos.y)) + 20;

  return `${minX} ${minY} ${maxX - minX} ${maxY - minY}`;
}
  numberToColor(value: number): string {
    switch (value) {
      case 1: return 'white';
      case 3: return 'aqua';
      case 5: return 'green';
      case 10: return 'yellow';
      case 9223372036854775807: return 'black';
      default: return 'white';
    }
  }
  colorToNumber(color: string): number {
    switch (color.toLowerCase()) {
      case 'white': return 1;
      case 'magenta': return 1;
      case 'red': return 1;
      case 'aqua': return 3;
      case 'green': return 5;
      case 'yellow': return 10;
      case 'black': return 9223372036854775807;
      default: return 0;
    }
  }

  isStart(index: number): boolean {
    if (!this.grid) return false;
    const [startX, startY] = this.grid.start;
    const width = this.grid.width;
    return index === startY * width + startX;
  }

  isEnd(index: number): boolean {
    if (!this.grid) return false;
    const [endX, endY] = this.grid.end;
    const width = this.grid.width;
    return index === endY * width + endX;
  }

  onSvgMouseDown(): void {
    this.isMouseDown = true;
  }

  onMouseDown(index: number): void {
    this.isMouseDown = true;
    this.changeHexagonColor(index);
  }

  onMouseUp(): void {
    this.isMouseDown = false;
  }

  onMouseOver(index: number): void {
    if (this.isMouseDown) {
      this.changeHexagonColor(index);
    }
  }

}