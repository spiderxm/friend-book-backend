from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import Friends
from .serializer import FriendSerializer, FollowsSerializer, FollowersSerializer, FollowSerializer, UnFriendSerializer
from rest_framework.permissions import IsAuthenticated


class FollowFriendView(GenericAPIView):
    serializer_class = FriendSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"followed": True}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UnfollowFriendView(GenericAPIView):
    serializer_class = UnFriendSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"unfollowed": True}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class GetFollowersDataView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get(self, request):
        followers = Friends.objects.all().filter(follows__username=request.user.username)
        response = {
            "followers": FollowersSerializer(followers, many=True).data
        }
        return Response(response, status=status.HTTP_200_OK)


class GetFollowingDataView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get(self, request):
        follows = Friends.objects.all().filter(follower__username=request.user.username)
        response = {
            "follows": FollowsSerializer(follows, many=True).data,
        }
        return Response(response, status=status.HTTP_200_OK)


class GetFollowersAndFollowersCountView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get(self, request):
        follows = Friends.objects.all().filter(follower__username=request.user.username)
        followers = Friends.objects.all().filter(follows__username=request.user.username)
        response = {
            "follows": len(follows),
            "followers": len(followers)
        }
        return Response(response, status=status.HTTP_200_OK)


class CheckFollowsView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    serializer_class = FollowSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            if Friends.objects.all().filter(follower__username=request.user.username,
                                            follows__username=username).exists():
                return Response({"follows": True}, status=status.HTTP_200_OK)
            else:
                return Response({"follows": False}, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
