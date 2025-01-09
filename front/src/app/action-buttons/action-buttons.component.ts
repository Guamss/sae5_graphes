import {Component, Input} from '@angular/core';
import {Grid} from "../model/grid";
import {GridService} from "../service/grid.service";

@Component({
    selector: 'app-action-buttons',
    imports: [],
    templateUrl: './action-buttons.component.html',
    standalone: true,
    styleUrl: './action-buttons.component.css'
})
export class ActionButtonsComponent {
    @Input() grid: Grid | undefined

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
            this.gridService.sendGridDijkstra(this.grid).subscribe({
                error: err => console.error(err.message)
            });
        } else {
            console.log("ya rien frr")
        }

    }
}
