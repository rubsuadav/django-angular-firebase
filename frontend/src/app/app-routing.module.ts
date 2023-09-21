import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ListPostComponent as list } from './list-post/list-post.component';
import { CreatePostComponent as create } from './create-post/create-post.component';
import { UpdatePostComponent as update } from './update-post/update-post.component';
import { PostDetailsComponent as details } from './post-details/post-details.component';
import { RegisterComponent as register } from './register/register.component';
import { LoginComponent as login } from './login/login.component';
import { authGuardGuard } from './auth-guard.guard';

const routes: Routes = [
  {
    path: 'posts',
    component: list,
  },
  {
    path: '',
    redirectTo: 'posts',
    pathMatch: 'full',
  },
  {
    path: 'posts/create',
    component: create,
    canActivate: [authGuardGuard],
  },
  {
    path: 'posts/update/:uid',
    component: update,
    pathMatch: 'full',
    canActivate: [authGuardGuard],
  },
  {
    path: 'posts/:uid',
    component: details,
    pathMatch: 'full',
  },
  {
    path: 'register',
    component: register,
  },
  {
    path: 'login',
    component: login,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
