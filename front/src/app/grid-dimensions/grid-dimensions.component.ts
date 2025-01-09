import { Component } from '@angular/core';

@Component({
  selector: 'app-grid-dimensions',
  imports: [],
  templateUrl: './grid-dimensions.component.html',
  standalone: true,
  styleUrl: './grid-dimensions.component.css'
})
export class GridDimensionsComponent {
  width: number = 2;
  height: number = 5;
  // grid: Grid;

  // updateGrid(width, height) {
  //   console.log(width, height);
  // }
  // TODO : update quand le formulaire fonctionnera avec les NG models, Exemple de quoi il ressemble atm :
  //<div>
  //   <label for="rows">Nombre de lignes :</label>
  //   <input id="rows" type="number" [(ngModel)]="grid.width" min="2" max="1000"/>
  //
  //   <label for="cols">Nombre de colonnes :</label>
  //   <input id="cols" type="number" [(ngModel)]="grid.height" min="2" max="1000"/>
  //
  //   <button (click)="updateGrid(grid.width, grid.height)">Générer la grille</button>
  // </div>

  sendData() {
    console.log("jenvoie")
  }

  updateGrid(width: number, height: number) {
    console.log(width,height)
  }
}
