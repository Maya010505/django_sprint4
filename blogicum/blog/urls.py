from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/create/", views.post_edit, name="create_post"),
    path("posts/<int:post_id>/", views.post_detail, name="detail_post"),
    path("posts/<int:post_id>/edit/", views.post_edit, name="edit_post"),
    path("posts/<int:post_id>/delete/", views.post_delete, name="delete_post"),
    path(
        "posts/<int:post_id>/comment/",
        views.CommentCreateView.as_view(),
        name="add_comment",
    ),
    path(
        "posts/<int:post_id>/edit_comment/<int:comment_id>/",
        views.comment_edit,
        name="edit_comment",
    ),
    path(
        "posts/<int:post_id>/delete_comment/<int:comment_id>",
        views.comment_delete,
        name="delete_comment",
    ),
    path("profile/edit/", views.profile_edit, name="edit_profile"),
    path("profile/<str:username>/", views.profile_info, name="profile"),
    path("category/<slug:category_slug>/", views.category_posts,
         name="category_posts"),
]
