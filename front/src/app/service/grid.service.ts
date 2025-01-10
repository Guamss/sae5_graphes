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
        return this.http.post<any>(`${this.apiUrlAlgo}/dfs`, { end_x: endX, end_y: endY, start_x: startX, start_y: startY });
    }

    runBFS(startX: number, startY: number, endX: number, endY: number): Observable<any> {
        return this.http.post<any>(`${this.apiUrlAlgo}/bfs`, { end_x: endX, end_y: endY, start_x: startX, start_y: startY });
    }

    runDijkstra(startX: number, startY: number, endX: number, endY: number): Observable<any> {
        return this.http.post<any>(`${this.apiUrlAlgo}/dijkstra`, { end_x: endX, end_y: endY, start_x: startX, start_y: startY });
    }

    runBellmanFord(startX: number, startY: number, endX: number, endY: number): Observable<any> {
        return this.http.post<any>(`${this.apiUrlAlgo}/bellman_ford`, { end_x: endX, end_y: endY, start_x: startX, start_y: startY });
    }

    runAStar(startX: number, startY: number, endX: number, endY: number): Observable<any> {
        return this.http.post<any>(`${this.apiUrlAlgo}/a_star`, { end_x: endX, end_y: endY, start_x: startX, start_y: startY });
    }

    runRandomWalk(startX: number, startY: number, endX: number, endY: number): Observable<any> {
        return this.http.post<any>(`${this.apiUrlAlgo}/random_walk`, { end_x: endX, end_y: endY, start_x: startX, start_y: startY });
    }
}