from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('<int:post_id>/<slug:post_slug>/', views.UserProfileView.as_view(), name="posts_detail"),
]
