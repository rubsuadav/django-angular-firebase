import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ListPostComponent as list } from './list-post/list-post.component';
import { CreatePostComponent as create } from './create-post/create-post.component';

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
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
