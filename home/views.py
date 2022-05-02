from django.shortcuts import render
from django.views import View
from posts.models import Post


class HomeView(View):
    def get(self, request):
        posts = Post.objects.order_by('-updated').all()
        return render(request, 'home/index.html', {"posts": posts})
