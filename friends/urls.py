from django.urls import path

from .views import FollowFriendView, GetFollowersDataView, GetFollowingDataView, GetFollowersAndFollowersCountView, \
    CheckFollowsView, UnfollowFriendView

urlpatterns = [
    path('follow/', FollowFriendView.as_view()),
    path('un-follow/', UnfollowFriendView.as_view()),
    path('following/', GetFollowingDataView.as_view()),
    path('followers/', GetFollowersDataView.as_view()),
    path('user-friends-count/', GetFollowersAndFollowersCountView.as_view()),
    path('do-you-follow/', CheckFollowsView.as_view())
]
