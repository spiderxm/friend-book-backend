from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .serializers import PostSerializer, AllPostSerializer, CommentSerializer
from .models import Post
from rest_framework import permissions
from .permissions import IsOwner


class PostListCreateView(ListCreateAPIView):
    """
    Create and List Posts of verified users
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class PostDetailApiView(RetrieveUpdateDestroyAPIView):
    """
    Update, Retrieve and Delete Posts of verified user
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class AllPostsView(ListAPIView):
    """
    Get All Posts created by the users
    """
    serializer_class = AllPostSerializer
    queryset = Post.objects.all()
