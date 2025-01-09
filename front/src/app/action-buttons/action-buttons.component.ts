import {Component, Input, Output, EventEmitter} from '@angular/core';
import {Grid} from "../model/grid";
import {GridService} from "../service/grid.service";

@Component({
    selector: 'app-action-buttons',
    imports: [],
    templateUrl: './action-buttons.component.html',
    standalone: true,
    styleUrls: ['./action-buttons.component.css'] // Correction ici
})
export class ActionButtonsComponent {
    @Input() grid: Grid | undefined
    @Output() gridChange = new EventEmitter<Grid>();

    constructor(private gridService: GridService) {
    }


    generateGrid() {
        console.log("generateGrid")
    }

    setStartMode() {
        console.log("setStartMode")
    }

    setEndMode() {
        console.log("setEndMode")
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
}
