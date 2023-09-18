import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Post } from './post';
import { Observable, map, switchMap } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class PostService {
  private baseUrl = 'http://localhost:8000/api/post';
  private authUrl = 'http://localhost:8000/api/register';
  private getUserUrl = 'https://randomuser.me/api/';

  constructor(private httpClient: HttpClient) {}

  generatePhone(): string {
    let phoneNumber = '';
    for (let i = 0; i < 9; i++) {
      if (i === 0) {
        phoneNumber += String(Math.floor(Math.random() * 2) + 6);
      } else {
        phoneNumber += String(Math.floor(Math.random() * 10));
      }
    }
    return phoneNumber;
  }

  generateData(): Observable<any> {
    return this.httpClient.get(this.getUserUrl).pipe(
      map((data: any) => {
        const nombre = data['results'][0]['name']['first'];
        const apellido = data['results'][0]['name']['last'];
        const correo = data['results'][0]['email'].replace('example', 'gmail');
        const telefono = this.generatePhone();
        const generatedData = {
          name: nombre,
          last_name: apellido,
          email: correo,
          password: 'admin2',
          phone_number: telefono,
        };
        return generatedData;
      })
    );
  }

  getToken(): Observable<any> {
    return this.generateData().pipe(
      switchMap((data: any) => {
        return this.httpClient.post(this.authUrl, data);
      })
    );
  }
  getAll(): Observable<Post[]> {
    return this.httpClient.get<Post[]>(`${this.baseUrl}`);
  }

  create(post: Post, token: string): Observable<Post> {
    return this.httpClient.post<Post>(`${this.baseUrl}`, post, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        Bearer: `Bearer ${token}`,
      }),
    });
  }
}
