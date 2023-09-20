import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService as auth } from '../auth.service';
import { User } from '../user';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
})
export class RegisterComponent implements OnInit {
  user: User = new User();
  error: string = '';
  formSubmitted: boolean = false;

  constructor(
    private router: Router,
    private authService: auth,
  ) {}

  ngOnInit(): void {}

  onSubmit(): void {
    this.formSubmitted = true;
    this.authService.register(this.user).subscribe({
      next: (token: any) => {
        localStorage.setItem('token', token['token']);
        this.router.navigate(['/posts']).then(() => {
          window.location.reload();
        });
      },
      error: (error) => {
        this.error = error.error;
        if (error.error === 'expected string or bytes-like object') {
          this.error = '';
        }
      },
    });
  }
}
