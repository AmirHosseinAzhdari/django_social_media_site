from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('/<slug:slug>/', views.UserProfileView.as_view(), name="user_register"),
]
