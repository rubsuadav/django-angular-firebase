import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Post } from './post';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class PostService {
  private baseUrl = 'http://localhost:8000/api/post';

  constructor(private httpClient: HttpClient) {}

  getAll(): Observable<Post[]> {
    return this.httpClient.get<Post[]>(`${this.baseUrl}`);
  }

  getPost(uid: string): Observable<Post> {
    return this.httpClient.get<Post>(`${this.baseUrl}/${uid}`);
  }

  create(post: Post, token: string): Observable<Post> {
    return this.httpClient.post<Post>(`${this.baseUrl}`, post, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        Bearer: `Bearer ${token}`,
      }),
    });
  }

  update(uid: string, post: Post, token: string): Observable<Post> {
    return this.httpClient.put<Post>(`${this.baseUrl}/${uid}`, post, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        Bearer: `Bearer ${token}`,
      }),
    });
  }

  delete(uid: string, token: string): Observable<any> {
    return this.httpClient.delete(`${this.baseUrl}/${uid}`, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        Bearer: `Bearer ${token}`,
      }),
    });
  }
}
