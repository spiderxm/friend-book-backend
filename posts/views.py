from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, \
    GenericAPIView
from .serializers import PostSerializer, AllPostSerializer, CommentSerializer, CommentDetailSerializer, LikeSerializer
from .models import Post, Comment
from rest_framework import permissions, status
from .permissions import IsOwner
from rest_framework.response import Response


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
        return self.queryset.filter(user=self.request.user).order_by('-created_at')


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
        if self.request.method == "GET":
            return self.queryset
        return self.queryset.filter(user=self.request.user)


class AllPostsView(ListAPIView):
    """
    Get All Posts created by the users
    """
    serializer_class = AllPostSerializer
    queryset = Post.objects.all().order_by('-created_at')


class CommentCreateView(CreateAPIView):
    """
    Create comment
    """
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentListView(ListAPIView):
    """
    Comment List
    """
    serializer_class = CommentDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Comment.objects.all()
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(post=self.kwargs.get("id")).order_by("-created_at")


class LikeView(GenericAPIView):
    """
    Like and dislike a post
    """
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            post = Post.objects.get(id=serializer.validated_data['id'])
            likes = list(post.likes)
            user = request.user
            if user.username in likes:
                likes.remove(user.username)
                post.likes = likes
                post.save()
                return Response({"like": False}, status=status.HTTP_202_ACCEPTED)
            else:
                likes.append(user.username)
                post.likes = likes
                post.save()
                return Response({"like": True}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
