import { Component, OnInit } from '@angular/core';
import { Post } from '../post';
import { ActivatedRoute, Router } from '@angular/router';
import { PostService as service } from '../post.service';

@Component({
  selector: 'app-update-post',
  templateUrl: './update-post.component.html',
})
export class UpdatePostComponent implements OnInit {
  uid: string;
  post: Post = new Post();

  constructor(
    private route: ActivatedRoute,
    private postService: service,
    private router: Router,
  ) {}
  ngOnInit(): void {
    this.getPost();
  }

  private getPost() {
    this.uid = this.route.snapshot.params['uid'];
    this.post = new Post();
    this.postService.getPost(this.uid).subscribe((data) => {
      this.post = data;
    });
  }

  goBack() {
    this.router.navigate(['/posts']);
  }

  private updatePost() {
    this.postService.update(this.uid, this.post).subscribe(() => {
      this.goBack();
    });
  }

  onSubmit(): void {
    this.updatePost();
  }
}
