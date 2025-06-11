from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Comment
from .utils import get_published_posts
from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm, PostForm, CommentsForm
from django.core.paginator import Paginator
from django.views.generic import CreateView
from django.db.models import Count

from django.utils import timezone


User = get_user_model()


def index(request):
    post_list = (
        get_published_posts()
        .select_related("category", "author", "location")
        .order_by("-pub_date")
        .annotate(comment_count=Count("comments"))
    )

    context = {
        "post_list": post_list,
    }

    paginator = Paginator(post_list, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context["page_obj"] = page_obj
    return render(request, "blog/index.html", context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related("category", "author", "location"),
        pk=post_id,
    )

    if not (
        post.is_published
        and post.category.is_published
        and post.pub_date <= timezone.now()
    ):
        if post.author != request.user:
            raise Http404

    form = CommentsForm()
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    comments = post.comments.all().order_by("created_at")

    context = {"post": post, "comments": comments, "form": form}
    return render(request, "blog/detail.html", context)


@login_required
def post_edit(request, post_id=None):

    if post_id is not None:
        instance = get_object_or_404(Post, pk=post_id)

        if instance.author != request.user:
            return redirect("blog:post_detail", post_id)
    else:
        instance = None

    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=instance
    )

    context = {
        "form": form,
    }

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()

        if post_id:
            return redirect("blog:post_detail", post_id)
        else:
            return redirect("blog:profile", request.user.username)

    return render(request, "blog/create.html", context)


def post_delete(request, post_id):
    instance = get_object_or_404(Post, pk=post_id)

    if instance.author != request.user:
        raise Http404

    form = PostForm(instance=instance)

    context = {"form": form}

    if request.method == "POST":
        instance.delete()
        return redirect("blog:index")

    return render(request, "blog/create.html", context)


def category_posts(request, category_slug):
    category = Category.objects.filter(slug=category_slug).first()
    if not category:
        post_list = []
    else:
        if not category.is_published:
            raise Http404("Категория не опубликована")

        post_list = (
            get_published_posts()
            .filter(category=category)
            .select_related("category", "author", "location")
        )
    context = {
        "post_list": post_list,
    }
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context["page_obj"] = page_obj
    return render(request, "blog/index.html", context)


def profile_info(request, username):
    profile = get_object_or_404(User, username=username)

    context = {
        "profile": profile,
    }

    if request.user.username == username:
        page_obj = (
            Post.objects.filter(author=profile)
            .order_by("-pub_date")
            .select_related("category", "location")
            .annotate(comment_count=Count("comments"))
        )
    else:
        page_obj = (
            Post.objects.filter(
                author=profile,
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now(),
            )
            .order_by("-pub_date")
            .select_related("category", "location")
            .annotate(comment_count=Count("comments"))
        )

    context["page_obj"] = page_obj

    paginator = Paginator(page_obj, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context["page_obj"] = page_obj
    return render(request, "blog/profile.html", context)


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("blog:profile", username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, "blog/user.html", {"form": form})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentsForm
    template_name = "blog/detail.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = post
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail",
                       kwargs={"post_id": self.kwargs["post_id"]})


@login_required
def comment_edit(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post__id=post_id)

    if comment.author != request.user:
        raise Http404

    if request.method == "POST":
        form = CommentsForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", post_id=post_id)
    else:
        form = CommentsForm(instance=comment)

    context = {"form": form, "comment": comment}

    return render(request, "blog/comment.html", context)


@login_required
def comment_delete(request, post_id, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id, post__id=post_id)

    if comment.author != request.user:
        raise Http404

    context = {"comment": comment}

    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id=post_id)

    return render(request, "blog/comment.html", context)


@login_required
def add_comment(request, post_id):

    post = get_object_or_404(Post, pk=post_id)

    form = CommentsForm(request.POST)
    if form.is_valid():

        comment = form.save(commit=False)

        comment.author = request.user

        comment.post = post

        comment.save()

    return redirect("blog:post_detail", post_id=post_id)
