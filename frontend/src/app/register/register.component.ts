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

  constructor(private roter: Router, private authService: auth) {}

  ngOnInit(): void {}

  onSubmit(): void {
    this.authService.register(this.user).subscribe((data: any) => {
      this.roter.navigate(['/posts']);
    });
  }
}
