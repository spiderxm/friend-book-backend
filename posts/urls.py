from django.urls import path
from .views import PostListCreateView, PostDetailApiView, AllPostsView

urlpatterns = [
    path('', PostListCreateView.as_view(), name="posts-create-list"),
    path('all/', AllPostsView.as_view(), name="all-posts"),
    path('<int:id>', PostDetailApiView.as_view()),
]
