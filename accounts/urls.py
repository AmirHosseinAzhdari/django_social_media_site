from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name="user_register"),
    path('login/', views.UserLoginView.as_view(), name="user_login"),
    path('logout/', views.UserLogoutView.as_view(), name="user_logout"),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name="user_profile"),
    path('reset/', views.UserPasswordResetView.as_view(), name="reset_password"),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name="reset_password_done"),
    path('confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(),
         name="reset_password_confirm"),
    path('confirm/complete/', views.UserPasswordResetCompleteView.as_view(), name="reset_password_complete"),
    path('follow/<int:user_id>/', views.UserFollowView.as_view(), name="user_follow"),
    path('unFollow/<int:user_id>/', views.UserUnFollowView.as_view(), name="user_unfollow"),
    path('edit-profile/', views.EditProfileView.as_view(), name="edit_profile"),
]
