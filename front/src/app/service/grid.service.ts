import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Grid } from '../model/grid';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root', // Permet l'injection dans les standalone components
})
export class GridService {
  private apiUrl = 'http://localhost:3000/dijkstra'; // URL de l'API

  constructor(private http: HttpClient) {}

  sendGridDijkstra(grid: Grid): Observable<any> {
    return this.http.post(this.apiUrl, grid);
  }
}
