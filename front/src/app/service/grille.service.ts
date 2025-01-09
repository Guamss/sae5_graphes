import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Grille } from '../model/grille';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root', // Permet l'injection dans les standalone components
})
export class GrilleService {
  private apiUrl = 'http://localhost:3000/dijkstra'; // URL de l'API

  constructor(private http: HttpClient) {}

  sendGridDijkstra(grid: Grille): Observable<any> {
    return this.http.post(this.apiUrl, grid);
  }
}
