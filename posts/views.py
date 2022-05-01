from django.shortcuts import render
from django.views import View

from posts.models import Post


class UserProfileView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, 'posts/detail.html', {"post": post})
