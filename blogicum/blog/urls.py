from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/create/", views.post_edit, name="post_create"),
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
    path("posts/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    path("posts/<int:post_id>/delete/", views.post_delete, name="post_delete"),
    path(
        "posts/<int:post_id>/comment/",
        views.CommentCreateView.as_view(),
        name="comment_add",
    ),
    path(
        "posts/<int:post_id>/edit_comment/<int:comment_id>/",
        views.comment_edit,
        name="comment_edit",
    ),
    path(
        "posts/<int:post_id>/delete_comment/<int:comment_id>",
        views.comment_delete,
        name="comment_delete",
    ),
    path("profile/edit/", views.profile_edit, name="edit_profile"),
    path("profile/<str:username>/", views.profile_info, name="profile"),
    path("category/<slug:category_slug>/", views.category_posts,
         name="category_posts"),
]
