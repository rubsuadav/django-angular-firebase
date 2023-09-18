from django.urls import path
from .views import PostListView

urlpatterns = [
    path('post', PostListView.as_view()),
    path('post/<str:post_id>', PostListView.as_view()),
]
