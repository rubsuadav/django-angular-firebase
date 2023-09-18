import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ListPostComponent as list } from './list-post/list-post.component';
import { CreatePostComponent as create } from './create-post/create-post.component';
import { UpdatePostComponent as update } from './update-post/update-post.component';
import { PostDetailsComponent as details } from './post-details/post-details.component';

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
  {
    path: 'posts/update/:uid',
    component: update,
    pathMatch: 'full',
  },
  {
    path: 'posts/:uid',
    component: details,
    pathMatch: 'full',
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
