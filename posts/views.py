from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from posts.forms import PostCreateAndUpdateForm, CommentCreateForm
from posts.models import Post, Comment, Vote


class PostDetailView(View):
    form_class = CommentCreateForm

    def setup(self, request, *args, **kwargs):
        self.model_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, post_id, post_slug, comment_id=None):
        comments = self.model_instance.pcomments.filter(is_reply=False)
        reply_comment = get_object_or_404(Comment, pk=comment_id) if comment_id else None
        user_can_like = False
        if request.user.is_authenticated and self.model_instance.user_can_like(user=request.user):
            user_can_like = True
        return render(request, 'posts/detail.html', {
            "post": self.model_instance,
            "comments": comments,
            'form': self.form_class,
            "reply": reply_comment,
            "user_can_like": user_can_like
        })

    @method_decorator(login_required)
    def post(self, request, post_id, post_slug, comment_id=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            if comment_id:
                new_comment.is_reply = True
                new_comment.reply = get_object_or_404(Comment, pk=comment_id)
            new_comment.user = request.user
            new_comment.post = self.model_instance
            new_comment.save()
            messages.success(request, "Comment added successfully", 'success')
            return redirect('posts:post_detail', self.model_instance.id, self.model_instance.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateAndUpdateForm

    def get(self, request):
        form = self.form_class
        return render(request, 'posts/create.html', {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["body"][:50])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'posts created successfully', 'success')
            return redirect('posts:post_detail', new_post.id, new_post.slug)
        return render(request, 'posts/update.html', {"form": form})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Your posts was deleted successfully', 'success')
        else:
            messages.error(request, 'You can not delete a posts that does not belong to you', 'danger')
        return redirect('accounts:user_profile', user_id=request.user.id)


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateAndUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'You can not update a posts that does not belong to you', 'danger')
            return redirect('accounts:user_profile', user_id=request.user.id)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'posts/update.html', {"form": form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:50])
            new_post.save()
            messages.success(request, 'posts updated successfully', 'success')
            return redirect('posts:post_detail', post.id, post.slug)
        return render(request, 'posts/update.html', {"form": form})


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        liked_post = post.pvote.filter(user=request.user)
        if liked_post:
            messages.error(request, "You are already liked this post", "danger")
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'You liked this post successfully', 'success')
        return redirect("posts:post_detail", post.id, post.slug)
