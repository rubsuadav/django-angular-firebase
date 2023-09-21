import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService as auth } from '../auth.service';
import { User } from '../user';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
})
export class LoginComponent implements OnInit {
  user: User = new User();
  error: string = '';
  formSubmitted: boolean = false;

  constructor(
    private router: Router,
    private authService: auth,
  ) {}

  ngOnInit() {}

  onSubmit(postForm: NgForm): void {
    this.formSubmitted = true;
    if (postForm.invalid) return;
    this.authService.login(this.user).subscribe({
      next: (token: any) => {
        localStorage.setItem('token', token['token']);
        this.router.navigate(['/posts']).then(() => {
          window.location.reload();
        });
      },
      error: (error) => {
        this.error = error.error;
        if (error.error.includes('No user record found for the provided email'))
          this.error = `No existe un usuario con el correo ${this.user.email}`;
      },
    });
  }
}
