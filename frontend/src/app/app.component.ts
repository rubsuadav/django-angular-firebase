import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
})
export class AppComponent implements OnInit {
  showRegisterButton: boolean = true;
  showLoginButton: boolean = true;
  showCreatePostButton: boolean = false;

  constructor() {}

  ngOnInit() {
    const token = localStorage.getItem('token');
    if (token) {
      this.showRegisterButton = false;
    }
    if (token && !this.showRegisterButton) {
      this.showLoginButton = false;
    }
    if (token && !this.showRegisterButton && !this.showLoginButton) {
      this.showCreatePostButton = true;
    }
  }
}
