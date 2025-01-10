import {Component, Input, Output, EventEmitter} from '@angular/core';
import {Grid} from "../model/grid";
import {GridService} from "../service/grid.service";

@Component({
    selector: 'app-action-buttons',
    imports: [],
    templateUrl: './action-buttons.component.html',
    standalone: true,
    styleUrls: ['./action-buttons.component.css']
})
export class ActionButtonsComponent {
    @Input() grid: Grid | undefined
    @Output() gridChange = new EventEmitter<Grid>();

    constructor(private gridService: GridService) {
    }

    sendGridData() {
        if (this.grid) {
            console.log(this.grid)
            this.gridService.sendWeightGrid(this.grid).subscribe({
                error: err => console.error(err.message)
            });
        } else {
            console.log("ya rien frr")
        }
    }
    generateGrid(): void {
        this.gridService.getGridWeights().subscribe({
            next: (weights) => {
                this.grid = {
                    height: weights.length,
                    width: weights[0]?.length || 0,
                    start: [weights[0]?.length - 1, 0], // Point d'arrivée par défaut
                    end: [0, weights.length - 1], // Point de départ par défaut
                    tab: weights
                };
                this.gridChange.emit(this.grid);
            },
            error: (err) => {
                console.error('Erreur lors du chargement des données de la grille:', err);
            }
        });
    }

    salut() {
        console.log('jai pas didentitée')
    }
}