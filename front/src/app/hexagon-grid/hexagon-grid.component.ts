import {Component, EventEmitter, OnDestroy, Output} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {Grid} from '../model/grid';
import {Subscription} from 'rxjs';

@Component({
    selector: 'app-hexagon-grid',
    imports: [CommonModule, FormsModule,],
    templateUrl: './hexagon-grid.component.html',
    standalone: true,
    styleUrl: './hexagon-grid.component.css'
})
export class HexagonGridComponent implements OnDestroy {
    @Output() newGrid = new EventEmitter<Grid>(); // Déclare l'@Output pour émettre le grid

    selectedColor: string = "white";
    colorWeightDict: any = {
        "white": 1,
        "green": 10,
        "aqua": 20,
        "yellow": 30,
        "black": 40
    };

    grid: Grid = {
        height: 5,
        width: 5,
        start: [0, 0],
        end: [4, 4],
        tab: []  // On garde ici les poids des hexagones
    };

    isSettingStart: boolean = false;
    isSettingEnd: boolean = false;
    subs: Subscription[] = [];

    constructor() {
        this.generateGrid();
    }

    generateGrid(): void {
        this.grid.tab = Array.from({length: this.grid.height}, () =>
            Array.from({length: this.grid.width}, () => 1) // Initialise les poids à 1
        );
        this.emitGrid();
    }

    getColorForWeight(weight: number): string {
        switch (weight) {
            case 1:
                return 'white';
            case 10:
                return 'green';
            case 20:
                return 'aqua';
            case 30:
                return 'yellow';
            case 40:
                return 'black';
            default:
                return 'grey';
        }
    }

    onHexClick(row: number, col: number): void {
        if (this.isSettingStart) {
            this.grid.start = [row, col];
            this.isSettingStart = false;
        } else if (this.isSettingEnd) {
            this.grid.end = [row, col];
            this.isSettingEnd = false;
        } else {
            this.grid.tab[row][col] = this.colorWeightDict[this.selectedColor];
        }
        this.emitGrid(); // Émet la grille mise à jour après un clic
    }

    updateGrid(rows: number, cols: number): void {
        this.grid.height = rows;
        this.grid.width = cols;
        this.generateGrid();
    }

    setStartMode(): void {
        this.isSettingStart = true;
        this.isSettingEnd = false;
    }

    setEndMode(): void {
        this.isSettingEnd = true;
        this.isSettingStart = false;
    }

    emitGrid(): void {
        this.newGrid.emit(this.grid); // Émet la grille actuelle
    }

    ngOnDestroy(): void {
        this.subs.forEach(sub => sub.unsubscribe());
    }
}