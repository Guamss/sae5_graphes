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
    @Output() sumWeightChange: EventEmitter<number> = new EventEmitter<number>();
    @Output() visitedChange: EventEmitter<Map<[number, number], [number, number]>> = new EventEmitter<Map<[number, number], [number, number]>>;
    @Output() solutionChange: EventEmitter<Map<[number, number], [number, number]>> = new EventEmitter<Map<[number, number], [number, number]>>;

    sumWeight: number = 0;
    visited: Map<[number, number], [number, number]> = new Map();
    solution: Map<[number, number], [number, number]> = new Map();

    constructor(private gridService: GridService) {
    }

    parseData(jsonData: any) {
        // Créer une map pour visited et solution
        const visitedMap: Map<[number, number], [number, number]> = new Map();
        const solutionMap: Map<[number, number], [number, number]> = new Map();

        // Fonction utilitaire pour extraire les coordonnées d'une clé
        const extractCoords = (key: string): [number, number] => {
            const state = key.split(' | ');
            const coords = state[1].slice(1, -1).split(',').map(Number);
            if (coords.length === 2) {
                return [coords[0], coords[1]];
            } else {
                throw new Error(`Coordonnées invalides : ${state[1]}`);
            }
        };

        // Traitement de la partie "solution"
        Object.keys(jsonData.solution).forEach((key) => {
            const [x, y] = extractCoords(key);
            const nextState = jsonData.solution[key].split(' | ');
            this.sumWeight += parseInt(nextState[0])
            const nextCoords: number[] = nextState[1].slice(1, -1).split(',').map(Number);

            if (nextCoords.length >= 2) {
                // Limiter à 2 éléments si plus
                const limitedNextCoords: [number, number] = [nextCoords[0], nextCoords[1]];
                solutionMap.set([x, y], limitedNextCoords);
            } else {
                console.error(`Coordonnées invalides pour la solution : ${nextState[1]}`);
            }
        });

        // Traitement de la partie "visited"
        Object.keys(jsonData.visited).forEach((key) => {
            const [x, y] = extractCoords(key);
            const nextStates: string[] = jsonData.visited[key];

            // Si des coordonnées suivantes existent, les ajouter à la map visited
            if (nextStates.length > 0) {
                const nextState = nextStates[0].split(' | ');
                const nextCoords: number[] = nextState[1].slice(1, -1).split(',').map(Number);

                if (nextCoords.length >= 2) {
                    // Limiter à 2 éléments si plus
                    const limitedNextCoords: [number, number] = [nextCoords[0], nextCoords[1]];
                    visitedMap.set([x, y], limitedNextCoords);
                } else {
                    console.error(`Coordonnées invalides pour visited : ${nextState[1]}`);
                }
            }
        });

        this.visited = visitedMap;
        this.solution = solutionMap;
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
                const resetWeights = weights.map(row => row.map(() => 1));

                this.grid = {
                    height: resetWeights.length,
                    width: resetWeights[0]?.length || 0,
                    start: [resetWeights[0]?.length - 1, 0], // Point d'arrivée par défaut
                    end: [0, resetWeights.length - 1], // Point de départ par défaut
                    tab: resetWeights
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
                    next: (result) => {
                        this.parseData(result)
                        this.visitedChange.emit(this.visited);
                        this.solutionChange.emit(this.solution);
                        this.sumWeightChange.emit(this.sumWeight);
                    },
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
                next: (result) => {
                    this.parseData(result)
                    this.visitedChange.emit(this.visited);
                    this.solutionChange.emit(this.solution);
                    this.sumWeightChange.emit(this.sumWeight);
                },
                error: (err) => console.error('Erreur lors de l\'exécution de BFS:', err)
            });
        }
    }

    runBellmanFord() {
        if (this.grid) {
            this.sendGridWeights();
            const {start, end} = this.grid;
            this.gridService.runBellmanFord(start[0], start[1], end[0], end[1]).subscribe({
                next: (result) => {
                    this.parseData(result)
                    this.visitedChange.emit(this.visited);
                    this.solutionChange.emit(this.solution);
                    this.sumWeightChange.emit(this.sumWeight);
                }, error: (err) => console.error('Erreur lors de l\'exécution de Bellman-Ford:', err)
            });
        }
    }

    runDijkstra() {
        if (this.grid) {
            this.sendGridWeights();
            const {start, end} = this.grid;
            this.gridService.runDijkstra(start[0], start[1], end[0], end[1]).subscribe({
                next: (result) => {
                    this.parseData(result)
                    this.visitedChange.emit(this.visited);
                    this.solutionChange.emit(this.solution);
                    this.sumWeightChange.emit(this.sumWeight);
                },
                error: (err) => console.error('Erreur lors de l\'exécution de Dijkstra:', err)
            });
        }
    }

    runAStar() {
        if (this.grid) {
            this.sendGridWeights();
            const {start, end} = this.grid;
            this.gridService.runAStar(start[0], start[1], end[0], end[1]).subscribe({
                next: (result) => {
                    this.parseData(result)
                    this.visitedChange.emit(this.visited);
                    this.solutionChange.emit(this.solution);
                    this.sumWeightChange.emit(this.sumWeight);
                }, error: (err) => console.error('Erreur lors de l\'exécution de A*:', err)
            });
        }
    }

    runRandomWalk() {
        if (this.grid) {
            this.sendGridWeights();
            const {start, end} = this.grid;
            this.gridService.runRandomWalk(start[0], start[1], end[0], end[1]).subscribe({
                next: (result) => {
                    this.parseData(result)
                    this.visitedChange.emit(this.visited);
                    this.solutionChange.emit(this.solution);
                    this.sumWeightChange.emit(this.sumWeight);
                }, error: (err) => console.error('Erreur lors de l\'exécution de Random Walk:', err)
            });
        }
    }
}