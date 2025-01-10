import {Component, EventEmitter, Output} from '@angular/core';
import {GridService} from "../service/grid.service";
import {FormsModule} from "@angular/forms";
import {Grid} from "../model/grid";
import {MessageService} from "primeng/api";
import {ToastModule} from "primeng/toast";

@Component({
    selector: 'app-grid-dimensions',
    imports: [
        FormsModule,
        ToastModule
    ],
    templateUrl: './grid-dimensions.component.html',
    standalone: true,
    styleUrl: './grid-dimensions.component.css'
})
export class GridDimensionsComponent {
    width: number = 0;
    height: number = 0;

    @Output() gridUpdated = new EventEmitter<Grid>();

    constructor(private gridService: GridService,
                private messageService: MessageService) {
    }


    ngOnInit(): void {
        this.gridService.getGridDimensions().subscribe({
            next: (dimensions) => {
                this.height = dimensions.height;
                this.width = dimensions.width;
            },
            error: () => {
                this.messageService.add({
                    severity: 'error',
                    summary: 'Erreur :(',
                    detail: 'Erreur lors de la récupération des dimensions de la grille.'
                });
            }
        });
    }

    // Méthode pour envoyer les nouvelles dimensions à l'API
    sendGrid(): void {
        this.gridService.sendGridDimensions(this.height, this.width).subscribe({
            next: () => {
                this.messageService.add({
                    severity: 'success',
                    summary: 'Succès !',
                    detail: '\'Dimensions de la grille envoyées avec succès !\''
                });
                // Créer une nouvelle grille avec les dimensions mises à jour
                const updatedGrid: Grid = {
                    width: this.width,
                    height: this.height,
                    start: [this.width - 1, 0], // Ajuster les coordonnées d'arrivée
                    end: [0, this.height - 1], // Ajuster les coordonnées de départ
                    tab: Array.from({length: this.height}, () => Array(this.width).fill(1)) // Initialize the tab array
                };
                this.gridUpdated.emit(updatedGrid);  // Émettre l'événement avec la nouvelle grille
            },
            error: () => {
                this.messageService.add({
                    severity: 'error',
                    summary: 'Erreur :(',
                    detail: 'Erreur lors de l\'envoi des dimensions.'
                });
            }
        });
    }
}