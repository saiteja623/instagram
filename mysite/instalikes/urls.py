from django.contrib import admin
from django.urls import path
from instalikes import views

urlpatterns = [
    path("", views.login, name="login"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("user_profile", views.user_profile, name="user_profile"),
    path("update_user", views.update_user, name="update_user"),
    path("homePage", views.homePage, name="homePage"),
    path("increaseLikes", views.increaseLikes, name="increaseLikes"),
    path("decreaseLikes", views.decreaseLikes, name="decreaseLikes"),
    path("checkForLike", views.checkForLike, name="checkForLike"),
    path("ajaxgetLikes", views.ajaxgetLikes, name="ajaxgetLikes"),
    path("send_request", views.send_request, name="send_request"),
    path("accept_request", views.accept_request, name="accept_request"),
    path("decline_request", views.decline_request, name="decline_request"),
    path("unsend_request", views.unsend_request, name="unsend_request"),
    path("friend_requests", views.friend_requests, name="friend_requests"),
    path("checkFriend", views.checkFriend, name="checkFriend"),
    path("remove_friend", views.remove_friend, name="remove_friend"),
    path(
        "update_userdesc_ajax", views.update_userdesc_ajax, name="update_userdesc_ajax"
    ),
    path("user_profile/<str:username>", views.homepage_user, name="homepage_user"),
    path("friend_requests/<str:username>", views.homepage_user, name="homepage_user"),
    path("homePage/<str:username>", views.homepage_user, name="homepage_user"),
    path("search_user", views.search_user, name="search_user"),
    path("create_post",views.create_post,name="create_post"),
    path("logout", views.logout, name="logout"),
]
