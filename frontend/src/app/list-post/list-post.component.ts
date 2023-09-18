import { Component, OnInit } from '@angular/core';
import { Post } from '../post';
import { PostService as service } from '../post.service';

@Component({
  selector: 'app-list-post',
  templateUrl: './list-post.component.html',
})
export class ListPostComponent implements OnInit {
  posts: Post[];
  constructor(private postServicio: service) {}

  ngOnInit(): void {
    this.getPosts();
  }

  private getPosts() {
    this.postServicio.getAll().subscribe((data) => {
      this.posts = data;
    });
  }
}
