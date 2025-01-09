import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Grid} from '../model/grid';
import {Observable} from 'rxjs';

@Injectable({
    providedIn: 'root', // Permet l'injection dans les standalone components
})
export class GridService {
    private apiUrl = 'http://localhost:5000/grid'; // URL de l'API

    constructor(private http: HttpClient) {
    }

    getGridDimensions(): Observable<{ height: number; width: number }> {
        return this.http.get<{ height: number; width: number }>(`${this.apiUrl}/dimensions`);
    }
    sendGridDimensions(height: number, width: number): Observable<any> {
        return this.http.put(`${this.apiUrl}/dimensions`, {"height": height, "width": width})
    }
    getGridWeights(): Observable<number[][]> {
        return this.http.get<number[][]>(`${this.apiUrl}/weights`);
    }
    sendWeightGrid(grid: Grid): Observable<any> {
        return this.http.put(`${this.apiUrl}/weights`, {"grid": grid.tab});
    }
}