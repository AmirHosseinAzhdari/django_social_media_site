from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace="home:home")),
    path('accounts/', include('accounts.urls', namespace="accounts:accounts")),
    path('posts/', include('posts.urls', namespace="posts:posts")),
]
