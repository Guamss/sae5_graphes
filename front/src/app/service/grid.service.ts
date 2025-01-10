import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Grid} from '../model/grid';
import {Observable} from 'rxjs';

@Injectable({
    providedIn: 'root', // Permet l'injection dans les standalone components
})
export class GridService {
    private apiUrlGrid = 'http://localhost:5000/grid'; // URL de l'
    private apiUrlAlgo = 'http://localhost:5000/algorithm'; // URL de l'API


    constructor(private http: HttpClient) {
    }

    getGridDimensions(): Observable<{ height: number; width: number }> {
        return this.http.get<{ height: number; width: number }>(`${this.apiUrlGrid}/dimensions`);
    }
    sendGridDimensions(height: number, width: number): Observable<any> {
        return this.http.put(`${this.apiUrlGrid}/dimensions`, {"height": height, "width": width})
    }
    getGridWeights(): Observable<number[][]> {
        return this.http.get<number[][]>(`${this.apiUrlGrid}/weights`);
    }
    sendWeightGrid(grid: Grid): Observable<any> {
        return this.http.put(`${this.apiUrlGrid}/weights`, {"grid": grid.tab});
    }

    runDFS(startX: number, startY: number, endX: number, endY: number): Observable<any> {
        return this.http.post(`${this.apiUrlAlgo}/dfs`, { start_x: startX, start_y: startY, end_x: endX, end_y: endY });
    }

    runBFS(startX: number, startY: number, endX: number, endY: number): Observable<any> {
        return this.http.post(`${this.apiUrlAlgo}/bfs`, { start_x: startX, start_y: startY, end_x: endX, end_y: endY });
    }

    runDijkstra(startX: number, startY: number, endX: number, endY: number): Observable<any> {
        return this.http.post(`${this.apiUrlAlgo}/dijkstra`, { start_x: startX, start_y: startY, end_x: endX, end_y: endY });
    }

    runBellmanFord(startX: number, startY: number, endX: number, endY: number): Observable<any> {
        return this.http.post(`${this.apiUrlAlgo}/bellman_ford`, { start_x: startX, start_y: startY, end_x: endX, end_y: endY });
    }

    runAStar(startX: number, startY: number, endX: number, endY: number): Observable<any> {
        return this.http.post(`${this.apiUrlAlgo}/a_star`, { start_x: startX, start_y: startY, end_x: endX, end_y: endY });
    }

    runRandomWalk(startX: number, startY: number, endX: number, endY: number): Observable<any> {
        return this.http.post(`${this.apiUrlAlgo}/random_walk`, { start_x: startX, start_y: startY, end_x: endX, end_y: endY });
    }
}