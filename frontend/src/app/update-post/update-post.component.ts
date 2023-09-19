import { Component, OnInit } from '@angular/core';
import { Post } from '../post';
import { ActivatedRoute, Router } from '@angular/router';
import { PostService as service } from '../post.service';
import { AuthService as auth } from '../auth.service';

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
    private authService: auth,
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

  onSubmit() {
    this.authService.getToken().subscribe((token: any) => {
      localStorage.setItem('token', token['token']);
      token = localStorage.getItem('token');
      this.postService.update(this.uid, this.post, token).subscribe(() => {
        this.goBack();
      });
    });
  }
}
