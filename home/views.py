from django.db.models import Q
from django.shortcuts import render
from django.views import View

from home.forms import PostSearchForm
from posts.models import Post


class HomeView(View):
    form_class = PostSearchForm

    def get(self, request):
        if request.GET.get("search"):
            search = request.GET.get("search")
            posts = Post.objects.filter(Q(title__icontains=search) | Q(body__icontains=search))
        else:
            posts = Post.objects.all()
        return render(request, 'home/index.html', {"posts": posts, "form": self.form_class})
