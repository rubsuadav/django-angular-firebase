import { Component, OnInit } from '@angular/core';
import { Post } from '../post';
import { PostService as service } from '../post.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-list-post',
  templateUrl: './list-post.component.html',
})
export class ListPostComponent implements OnInit {
  posts: Post[];

  constructor(
    private router: Router,
    private postServicio: service,
  ) {}

  ngOnInit(): void {
    this.getPosts();
  }

  showPost(uid: string): void {
    this.router.navigate(['posts/', uid]);
  }

  editPost(uid: string): void {
    this.router.navigate(['posts/update', uid]);
  }

  deletePost(uid: string): void {
    this.postServicio.delete(uid).subscribe(() => {
      this.getPosts();
    });
  }

  private getPosts() {
    this.postServicio.getAll().subscribe((data) => {
      this.posts = data;
    });
  }
}
