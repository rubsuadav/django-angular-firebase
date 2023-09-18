import { Component, OnInit } from '@angular/core';
import { Post } from '../post';
import { ActivatedRoute, Router } from '@angular/router';
import { PostService as service } from '../post.service';

@Component({
  selector: 'app-post-details',
  templateUrl: './post-details.component.html',
})
export class PostDetailsComponent implements OnInit {
  uid: string;
  post: Post;

  constructor(
    private route: ActivatedRoute,
    private postService: service,
    private router: Router
  ) {}
  ngOnInit(): void {
    this.getPost();
  }

  goBack() {
    this.router.navigate(['/posts']);
  }

  private getPost() {
    this.uid = this.route.snapshot.params['uid'];
    this.post = new Post();
    this.postService.getPost(this.uid).subscribe((data) => {
      this.post = data;
    });
  }
}
