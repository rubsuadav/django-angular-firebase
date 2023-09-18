import { Component, OnInit } from '@angular/core';
import { Post } from '../post';
import { PostService as service } from '../post.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-post',
  templateUrl: './create-post.component.html',
})
export class CreatePostComponent implements OnInit {
  post: Post = new Post();

  constructor(private postService: service, private roter: Router,) {}

  ngOnInit(): void {}

  private savePost() {
    this.postService.getToken().subscribe((token: any) => {
      localStorage.setItem('token', token['token']);
      token = localStorage.getItem('token');
      this.postService.create(this.post, token).subscribe(() => {
        this.goToPostList();
      });
    });
  }

  goToPostList() {
    this.roter.navigate(['/posts']);
  }

  onSubmit(): void {
    this.savePost();
  }
}
