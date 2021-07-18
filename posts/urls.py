from django.urls import path
from .views import PostListCreateView, PostDetailApiView, AllPostsView, CommentCreateView, CommentListView, LikeView

urlpatterns = [
    path('', PostListCreateView.as_view(), name="posts-create-list"),
    path('all/', AllPostsView.as_view(), name="all-posts"),
    path('<int:id>', PostDetailApiView.as_view()),
    path('comment/', CommentCreateView.as_view()),
    path('like/', LikeView.as_view()),
    path('<int:id>/comments/', CommentListView.as_view()),
]
