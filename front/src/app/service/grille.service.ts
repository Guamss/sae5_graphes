import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Grille} from '../model/grille';

@Injectable({
  providedIn: 'root'
})
export class GrilleService {
  apiUrl: string = "http://localhost:5000";

  constructor(private httpClient: HttpClient) {}

  sendGridDijkstra(grid: Grille): Observable<any> {
    return this.httpClient.post<any>(`${this.apiUrl}/dijkstra`, grid);
  }
}
