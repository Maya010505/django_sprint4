from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Post, Comment

User = get_user_model()


class ProfileEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "text", "pub_date", "location", "category", "image")
        widgets = {"birthday": forms.DateInput(attrs={"type": "date"})}


class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)
