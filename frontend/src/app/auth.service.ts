import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, throwError } from 'rxjs';
import { User } from './user';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(private httpClient: HttpClient) {}

  private registerUrl = 'http://localhost:8000/api/register';
  private loginUrl = 'http://localhost:8000/api/login';

  register(user: User): Observable<any> {
    return this.httpClient.post<User>(this.registerUrl, user).pipe(
      catchError((error) => {
        return throwError(() => error.error);
      })
    );
  }

  login(user: User): Observable<any> {
    return this.httpClient.post<User>(this.loginUrl, user).pipe(
      catchError((error) => {
        return throwError(() => error.error);
      })
    );
  }
}
