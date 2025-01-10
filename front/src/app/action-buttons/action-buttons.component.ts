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

    sendGridWeights() {
    if (!this.grid) {
        console.log("Grille non définie");
        return;
    }
    console.log('Grid before sending weights:', this.grid);
    this.gridService.sendWeightGrid(this.grid).subscribe({
        next: () => console.log('Grid weights sent successfully'),
        error: (err) => console.error('Error sending grid data:', err.message)
    });
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

    async runDFS() {
        if (this.grid) {
            try {
                await this.sendGridWeights();
                const {start, end} = this.grid;
                console.log('Start:', start, 'End:', end);
                console.log('Grid:', this.grid.tab);
                this.gridService.runDFS(start[0], start[1], end[0], end[1]).subscribe({
                    next: (result) => console.log('DFS Result:', result),
                    error: (err) => console.error('Erreur lors de l\'exécution de DFS:', err)
                });
            } catch (err) {
                console.error('Erreur lors de l\'envoi des poids de la grille:', err);
            }
        }
    }

    runBFS() {
        if (this.grid) {
            this.sendGridWeights();
            const {start, end} = this.grid;
            this.gridService.runBFS(start[0], start[1], end[0], end[1]).subscribe({
                next: (result) => console.log('BFS Result:', result),
                error: (err) => console.error('Erreur lors de l\'exécution de BFS:', err)
            });
        }
    }

    runBellmanFord() {
        if (this.grid) {
            this.sendGridWeights();
            const {start, end} = this.grid;
            this.gridService.runBellmanFord(start[0], start[1], end[0], end[1]).subscribe({
                next: (result) => console.log('Bellman-Ford Result:', result),
                error: (err) => console.error('Erreur lors de l\'exécution de Bellman-Ford:', err)
            });
        }
    }

    runDijkstra() {
        if (this.grid) {
            this.sendGridWeights();
            const {start, end} = this.grid;
            this.gridService.runDijkstra(start[0], start[1], end[0], end[1]).subscribe({
                next: (result) => console.log('Dijkstra Result:', result),
                error: (err) => console.error('Erreur lors de l\'exécution de Dijkstra:', err)
            });
        }
    }

    runAStar() {
        if (this.grid) {
            this.sendGridWeights();
            const {start, end} = this.grid;
            this.gridService.runAStar(start[0], start[1], end[0], end[1]).subscribe({
                next: (result) => console.log('A* Result:', result),
                error: (err) => console.error('Erreur lors de l\'exécution de A*:', err)
            });
        }
    }

    runRandomWalk() {
        if (this.grid) {
            this.sendGridWeights();
            const {start, end} = this.grid;
            this.gridService.runRandomWalk(start[0], start[1], end[0], end[1]).subscribe({
                next: (result) => console.log('Random Walk Result:', result),
                error: (err) => console.error('Erreur lors de l\'exécution de Random Walk:', err)
            });
        }
    }
}