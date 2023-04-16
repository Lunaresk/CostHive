import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import { throwError } from 'rxjs';
import {API_URL} from '../env';
import {User} from './user.model';
import { catchError } from 'rxjs/operators';

@Injectable()
export class UsersApiService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    return throwError(() => (err.message || 'Error: Unable to complete request.'));
    
  }

  // GET list of public, future events
  getExams(): Observable<User[]> {
    return this.http
      .get<User[]>(`${API_URL}/test`)
      .pipe(catchError(UsersApiService._handleError));
  }
}