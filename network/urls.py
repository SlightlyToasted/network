
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("users/<str:username>/page<int:page_num>", views.user, name="user"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("following/<int:page_num>", views.following, name="following"),
    path("all-posts/<int:page_num>", views.all_posts, name="all_posts"),

     # API Routes
    path("posts", views.create, name="create"),
    path("posts/posts", views.posts, name="posts"),
]
