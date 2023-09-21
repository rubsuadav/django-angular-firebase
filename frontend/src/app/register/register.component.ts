import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService as auth } from '../auth.service';
import { User } from '../user';
import { NgForm } from '@angular/forms';

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

  onSubmit(postForm: NgForm): void {
    this.formSubmitted = true;
    if (postForm.invalid) return;
    this.authService.register(this.user).subscribe({
      next: (token: any) => {
        localStorage.setItem('token', token['token']);
        this.router.navigate(['/posts']).then(() => {
          window.location.reload();
        });
      },
      error: (error) => {
        this.error = error.error;
        if (
          error.error ===
          'The user with the provided email already exists (EMAIL_EXISTS).'
        ) {
          this.error = 'El usuario con el correo proporcionado ya existe.';
          this.formSubmitted = true;
        } else if (
          error.error ===
          'The user with the provided phone number already exists (PHONE_NUMBER_EXISTS).'
        ) {
          this.error =
            'El usuario con el número de teléfono proporcionado ya existe.';
          this.formSubmitted = true;
        }
      },
    });
  }
}
